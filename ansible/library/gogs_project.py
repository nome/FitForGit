#!/usr/bin/python
# (c) 2017, Knut Franke <knut.franke@gmx.de>

DOCUMENTATION = '''
---
module: gogs_project
short_description: Creates/deletes Gogs Projects
description:
  - When the project does not exist in Gogs, it will be created.
  - When the project does exist and state=absent, it will be deleted.
  - Gogs API does not allow updating project settings.
author: "Knut Franke"
options:
  server_url:
    description: URL of Gogs server, with protocol (http or https)
    required: true
  login_user:
    description: Name of Gogs user ownning the project.
    required: true
  login_password:
    description: Password of Gogs user owning the project.
    required: true
  state:
    description:
      - If 'present', the project will be created or updated.
      - If 'absent', the user will be deleted.
    required: false
    default: present
    choices: ["present", "absent"]
  name:
    description: Name of Gogs project to be created/updated/deleted.
    required: true
  description:
    description: A short description of the project
    required: false
  public:
    description: Whether the project should be public or private.
    required: false
    default: false
    type: bool
  auto_init:
    description: If true and the project is new, create an initial commit with
      README, .gitignore and LICENSE.
    required: false
    default: false
    type: bool
  gitignores:
    description: Desired language .gitignore templates to apply. Use the name
      of the templates. For example, "Go" or "Go,SublimeText".
    required: false
  license:
    description: Desired LICENSE template to apply. Use the name of the
      template. For example, "Apache v2 License" or "MIT License".
    require: false
  readme:
    description: Desired README template to apply. Use the name of the
      template. Default is `Default`.
    required: false
  import_url:
    description: Git repository which will me imported into Gogs. Gogs server
      needs read access to this git repository.
    required: false
  import_username:
    description: Username for accessing import_url.
    required: false
  import_password:
    description: Password for accessing import_url.
    required: false
  mirror:
    description: Project will be a mirror of import_url.
    required: false
  mirror_sync:
    description: If the mirror project already exists, perform a sync (with the
      url set in Gogs, which might differ from import_url)
    required: false
  group:
    description: The group/organization this project belongs to. When not
      provided, project will belong to the user which is configured in
      'login_user'.
  sshkey_name:
    description: A name/title for the SSH deploy key to distinguish it from
      other deploy keys of the same project.
    required: false
    aliases:
      deploy_key_name
  sshkey_file:
    description: SSH public deploy key.
    required: false
    aliases:
      sshkey
      deploy_key
'''

RETURN = '''
result:
  description: Short description of applied changes.
  returned: changed
  type: string
  sample: Project created.
'''

EXAMPLES = '''
- name: Create Gogs project 'Hello-World'
  local_action:
    module: gogs_project
    server_url: https://gogs.example.com
    login_user: gogsuser
    login_password: secret
    name: Hello-World
'''

from ansible.module_utils.basic import *
from ansible.module_utils.urls import fetch_url, url_argument_spec
import json


def rest_request(module, method, path, body=None):
  """
  Generic REST API wrapper.

  `module` is the AnsibleModule instance from which `server_url` and other
  fetch parameters are read.

  `method` is the HTTP method (GET/POST/PATCH/DELETE)

  `path` is the resource path, relative to `module.params['server_url']`.

  `body` is the request body for POST/PATCH, as a Python dict/list. It will be
  converted to JSON before sending to the server.
  """
  url = module.params['server_url']
  if not url.endswith("/"):
    url += "/"
  url += path

  data = None
  headers = {}
  if body:
    data = json.dumps(body)
    headers["Content-Type"] = "application/json"

  resp, info = fetch_url(module, url, method=method, data=data,
    headers=headers, timeout=module.params['timeout'])

  info["request_body"] = body
  if body and "password" in body:
    info["request_body"]["password"] = "********"

  try:
    content = resp.read()
  except AttributeError:
    content = info.pop('body', '')

  if content:
    return info, json.loads(content)
  else:
    return info, None


def main():
  argument_spec = url_argument_spec()
  argument_spec.update({
    "server_url": dict(required=True),
    "url_username": dict(required=True, aliases=["login_user"]),
    "url_password": dict(required=True, aliases=["login_password"]),
    "timeout": dict(default=30, type='int'),
    "force_basic_auth": dict(default=True, type='bool'),
    "state": dict(default="present", choices=["present", "absent"]),
    "name": dict(required=True),
    "description": dict(),
    "public": dict(type='bool', default=False),
    "auto_init": dict(type='bool'),
    "gitignores": dict(),
    "license": dict(),
    # API docs suggest that the readme parameter can be omitted, but doing so
    # results in an error when auto_init=true (Gogs 0.10.18), so we set the
    # default here.
    "readme": dict(default="Default"),
    "import_url": dict(),
    "import_username": dict(),
    "import_password": dict(),
    "mirror": dict(type='bool', default=False),
    "mirror_sync": dict(type='bool', default=False),
    "group": dict(aliases=["organization"]),
    "sshkey_name": dict(aliases=["deploy_key_name"]),
    # sshkey_file is a bit of a misnomer, but we attempt to be compatible with
    # gitlab_user
    "sshkey_file": dict(aliases=["sshkey", "deploy_key"]),
  })
  module = AnsibleModule(
    argument_spec=argument_spec,
    supports_check_mode=False
  )

  # sanity check arguments
  if module.params["mirror"] and not module.params["import_url"]:
    module.fail_json(msg="mirror enabled but no import_url given")
  if module.params["mirror_sync"] and not module.params["mirror"]:
    module.fail_json(msg="mirror_sync requested, but mirror is disabled")
  if module.params["sshkey_name"] and not module.params["sshkey_file"]:
      module.fail_json(msg="sshkey_name given without sshkey_file")
  if module.params["sshkey_file"] and not module.params["sshkey_name"]:
      module.fail_json(msg="sshkey_file given without sshkey_name")

  if module.params["group"]:
    repopath = module.params["group"] + "/" + module.params["name"]
  else:
    repopath = module.params["url_username"] + "/" + module.params["name"]

  # get current repo state
  info, response = rest_request(module, "GET", "api/v1/repos/" + repopath)
  if info["status"] == 200:
    repo_exists = True
    old_state = response
  elif info["status"] == 404:
    repo_exists = False
    old_state = {}
  else:
    module.fail_json(msg="Error querying Gogs project: %s" % info["msg"], info=info)

  # if state=absent, we only need to delete the repo
  if module.params["state"] == "absent":
    if repo_exists:
      info, response = rest_request(module, "DELETE", "api/v1/repos/" + repopath)
      if info["status"] == 204:
        module.exit_json(changed=True, result="Successfully deleted project %s" % repopath)
      else:
        module.fail_json(msg="Failed to delete project %s: %s" % (repopath, info["msg"]), info=info)
    else:
      module.exit_json(changed=False, result="Project %s already deleted" % repopath)

  # if state=present, we may also need to update the project's parameters
  changed = False
  result = []

  if not repo_exists:
    # create repo
    if module.params["import_url"] is None:
      # create a new repository
      if module.params["group"]:
        path = "api/v1/org/%s/repos" % module.params["group"]
      else:
        path = "api/v1/user/repos"
      repo_params = {
        "name": "name",
        "description": "description",
        "auto_init": "auto_init",
        "gitignores": "gitignores",
        "license": "license",
        "readme": "readme",
      }
    else:
      # migrate/mirror repository from import_url
      path = "api/v1/repos/migrate"
      repo_params = {
        "clone_addr": "import_url",
        "auth_username": "import_username",
        "auth_password": "import_password",
        "uid": "url_username",
        "repo_name": "name",
        "mirror": "mirror",
        "description": "description",
      }
      if module.params["group"]:
        repo_params["uid"] = "group"

    create_params = {}
    if module.params["public"] is not None:
      create_params["private"] = not module.params["public"]
    for gogs_param, mod_param in repo_params.iteritems():
      if module.params[mod_param] is not None:
        create_params[gogs_param] = module.params[mod_param]

    info, response = rest_request(module, "POST", path, create_params)
    if info["status"] != 201:
      module.fail_json(msg="Failed to create project %s: %s" %
        (repopath, info["msg"]), info=info)
    changed = True
    result.append("Project created.")

  # update ssh key, if necessary
  if module.params["sshkey_name"] and module.params["sshkey_file" ]:
    info, response = rest_request(module, "GET" "api/v1/%s/keys" % repopath)
    if info["status"] != 200:
      module.fail_json(msg="Failed to get SSH keys for project %s: %s" %
        (repopath, info["msg"]), info=info)
    for entry in response:
      if entry["key"] == module.params["sshkey_file"]:
        break
    else:
      # no matching entry found, need update
      info, response = rest_request(module, "POST", "api/v1/repos/%s/keys" % repopath, {
        "title": module.params["sshkey_name"],
        "key": module.params["sshkey_file"]
      })
      if info["status"] != 201:
	module.fail_json(msg="Failed to set deploy key '%s' for project %s: %s" %
          (module.params["sshkey_name"], repopath, info["msg"]), info=info)
      changed = True
      result.append("Deploy key updated.")

  # execute mirror_sync, if requested
  if repo_exists and module.params["mirror_sync"]:
    info, response = rest_request(module, "POST", "api/v1/repos/" + repopath + "/mirror-sync")
    if info["status"] == 404:
      module.fail_json(msg="Project %s is not a mirror (according to Gogs)." %
        repo_path, info=info)
    elif info["status"] != 202:
      module.fail_json(msg="Failed to sync mirror %s: %s" %
        (repopath, info["msg"]), info=info)
    changed = True
    result.append("Project synced.")

  if changed:
    module.exit_json(changed=True, result=" ".join(result))
  else:
    module.exit_json(changed=False)

if __name__ == '__main__':
  main()
