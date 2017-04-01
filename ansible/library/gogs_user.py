#!/usr/bin/python
# (c) 2017, Knut Franke <knut.franke@gmx.de>

DOCUMENTATION = '''
---
module: gogs_user
short_description: Creates/updates/deletes Gogs Users
description:
  - When the user does not exist in Gogs, it will be created.
  - When the user does exist and state=absent, it will be deleted.
  - When changes are made to the user, it will be updated; but due to
    limitations in the Gogs API, the fact that changes were made will not
    always be reported back correctly.
author: "Knut Franke"
requirements:
  - An administrative user on the Gogs server.
options:
  server_url:
    description: URL of Gogs server, with protocol (http or https)
    required: true
  login_user:
    description: Name of administrative Gogs user.
    required: true
  login_password:
    description: Password of administrative Gogs user.
    required: true
  state:
    description:
      - If 'present', the user will be created or updated. For creating a new
        user, 'password' and 'email' must be given.
      - If 'absent', the user will be deleted.
    required: false
    default: present
    choices: ["present", "absent"]
  name:
    description: Name of Gogs user to be created/updated/deleted.
    required: true
  password:
    description: Password of Gogs user to be created/updated/deleted.
    required: false
  email:
    description: The email address that belongs to the user.
    required: false
  sshkey_name:
    description: A name/title for the SSH key to distinguish it from other keys of the same user.
    required: false
  sshkey_file:
    description: SSH public key of the user.
    required: false
    aliases:
      sshkey
  full_name:
    description: Full name of the user (for profile)
    required: false
  website:
    description: Web site belonging to the user (for profile)
    required: false
  location:
    description: Physical location of the user (for profile)
    required: false
  admin:
    description: Promote/demote user as Gogs site admin.
    required: false
    default: false
  allow_git_hook:
    description: Allow or disallow the user to create Git hooks. This
      effectively gives the user shell access to the account under which Gogs is
      running.
    required: false
    default: false
  allow_import_local:
    description: Allow or disallow the user to import Git repositories located
      on the server.
    required: false
    default: false
'''

RETURN = '''
result:
  description: Short description of applied changes.
  returned: changed
  type: string
  sample: User created. SSH key updated.
'''

EXAMPLES = '''
- name: Create Gogs user 'jessica'
  local_action:
    module: gogs_user
    server_url: https://gogs.example.com
    login_user: gogsadmin
    login_password: secret
    name: jessica
    password: jessicaspassword
    email: jessica@example.com

- name: Delete Gogs user 'james'
  local_action:
    module: gogs_user
    server_url: https://gogs.example.com
    login_user: gogsadmin
    login_password: secret
    name: james
    state: absent

- name: Create Gogs user 'john' and add his default SSH key
  local_action:
    module: gogs_user
    server_url: https://gogs.example.com
    login_user: gogsadmin
    login_password: secret
    name: john
    password: johnspassword
    email: john@example.com
    sshkey_name: default
    sshkey_file: "{{ lookup('file', '/home/john/.ssh/id_ed25519.pub') }}"
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
    "timeout": dict(required=False, default=30, type='int'),
    "force_basic_auth": dict(required=False, default=True),
    "state": dict(default="present", choices=["present", "absent"]),
    "username": dict(required=True, aliases=["name"]),
    "password": dict(required=False),
    "email": dict(required=False),
    "sshkey_name": dict(required=False),
    # sshkey_file is a bit of a misnomer, but we attempt to be compatible with
    # gitlab_user
    "sshkey_file": dict(required=False, aliases=["sshkey"]),
    "full_name": dict(required=False),
    "website": dict(required=False),
    "location": dict(required=False),
    "admin": dict(required=False, type='bool'),
    "allow_git_hook": dict(required=False, type='bool'),
    "allow_import_local": dict(required=False, type='bool'),
  })
  module = AnsibleModule(
    argument_spec=argument_spec,
    supports_check_mode=False
  )

  if module.params["sshkey_name"] and not module.params["sshkey_file"]:
      module.fail_json(msg="sshkey_name given without sshkey_file")
  if module.params["sshkey_file"] and not module.params["sshkey_name"]:
      module.fail_json(msg="sshkey_file given without sshkey_name")

  username = module.params["username"]

  # get current user state
  info, response = rest_request(module, "GET", "api/v1/users/" + username)
  if info["status"] == 200:
    user_exists = True
    old_state = response
  elif info["status"] == 404:
    user_exists = False
    old_state = {}
  else:
    module.fail_json(msg="Error querying Gogs server: %s" % info["msg"], info=info)

  # if state=absent, we only need to delete the user
  if module.params["state"] == "absent":
    if user_exists:
      info, response = rest_request(module, "DELETE", "api/v1/admin/users/" + username)
      if info["status"] == 204:
        module.exit_json(changed=True, result="Successfully deleted user %s" % username)
      else:
        module.fail_json(msg="Failed to delete user %s: %s" % (username, info["msg"]), info=info)
    else:
      module.exit_json(changed=False, result="User %s already deleted" % username)

  # if state=present, we may also need to update the user's parameters
  changed = False
  result = []

  if not user_exists:
    if not module.params["password"] or not module.params["email"]:
      module._fail_json(msg="If state=present (default), password and email must be given.")

    # create user
    info, response = rest_request(module, "POST", "api/v1/admin/users", {
      "username": username,
      "email": module.params["email"],
      "password": module.params["password"]
    })
    if info["status"] != 201:
      module.fail_json(msg="Failed to create user %s: %s" % (username, info["msg"]), info=info)
    changed = True
    result.append("User created.")

  # update the parameters we can set via /admin/users/:username
  user_params = ("email", "password", "full_name", "website", "location",
    "admin", "allow_git_hook", "allow_import_local")
  if user_exists or any(module.params[param] for param in user_params):
    new_state = {}

    # FIXME: Gogs API appears to be missing a way to query most of these settings, so
    # we can't tell whether they changed.
    for param in user_params:
      if not module.params[param]:
        continue
      if param in old_state:
        if old_state[param] != module.params[param]:
          new_state[param] = module.params[param]
          changed = True
      else:
        new_state[param] = module.params[param]

    # Gogs API requires the email address for updates, even if it didn't change
    if not "email" in new_state:
      new_state["email"] = old_state["email"]

    info, response = rest_request(module, "PATCH", "api/v1/admin/users/" + username, new_state)
    if info["status"] != 200:
      module.fail_json(msg="Failed to update user %s: %s" % (username, info["msg"]), info=info)

  # update ssh key, if necessary
  if module.params["sshkey_name"] and module.params["sshkey_file" ]:
    info, response = rest_request(module, "GET", "api/v1/users/%s/keys" % username)
    if info["status"] != 200:
      module.fail_json(msg="Failed to get SSH keys for user %s: %s" % (username, info["msg"]), info=info)
    for entry in response:
      if entry["key"] == module.params["sshkey_file"]:
        break
    else:
      # no matching entry found, need update
      info, response = rest_request(module, "POST", "api/v1/admin/users/%s/keys" % username, {
        "title": module.params["sshkey_name"],
        "key": module.params["sshkey_file"]
      })
      if info["status"] != 201:
	module.fail_json(msg="Failed to set SSH key '%s' for user %s: %s" %
          (module.params["sshkey_name"], username, info["msg"]), info=info)
      changed = True
      result.append("SSH key updated.")

  if changed:
    module.exit_json(changed=True, result=" ".join(result))
  else:
    module.exit_json(changed=False)

if __name__ == '__main__':
  main()
