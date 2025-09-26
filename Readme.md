# Discord Bot
### Status: Under Development

---

## HELP

```bash
!help -h            # Shows bot commands and usage
!create -h         # Help for creating roles, categories, and channels
!edit -h           # Help for editing roles
!assign -h         # Help for assigning roles to users or categories
!revoke -h         # Help for revoking roles from users or categories
!delete -h         # Help for deleting roles, categories, or channels
```

---

### CREATE COMMANDS

```pgsql
!create role {role_name} [#hex_color]           
!create category {category_name}                
!create text {channel_name} [-c category_name] 
!create voice {channel_name} [-c category_name]
```

### Examples

```pgsql
!create role Member
!create role Moderator #ff0000
!create category Projects
!create text general -c Projects
!create voice Lobby -c Projects
```
---

### EDIT ROLE COMMANDS

```pgsql
!edit role {role_name} name {new_name}           
!edit role {role_name} color {#hex_color}       
!edit role {role_name} permission {perm_name}   
!edit role {role_name} -p {perm_name}           
!edit role {role_name} set {default/moderator/admin} 
```

### Role permission shortcuts:

| Shortcut  | Permissions Applied                                    |
| --------- | ------------------------------------------------------ |
| default   | view/read/send/connect/speak                           |
| moderator | default + manage_messages/timeout_members              |
| admin     | moderator + manage_channels/manage_roles/administrator |

Available Permissions (`perm_aliases`):

```
kick, ban, manage, admin, mention, hoist, manage_roles, manage_channels,
read, send, embed, attach, voice, speak, mute, deafen, move, priority
```

### Examples:

```pgsql
!edit role Member name NewMember
!edit role Moderator color #00ff00
!edit role Moderator set moderator
!edit role Admin permission kick
```

---

### ASSIGN COMMANDS

```pgsql
!assign {@user} {role_name}                     
!assign role {role_name} -c {category_name}     
```

### Examples:

```sql
!assign @John Member
!assign role Member -c Projects
!assign role Moderator -c Staff Channels
```
- Assigning a role to a category grants view, send, connect, speak permissions to all channels in that category.

---

### REVOKE COMMANDS

```pgsql
!revoke {@user} {role_name}                     
!revoke role {role_name} -c {category_name}     
```

### Examples:
```sql
!revoke @John Member
!revoke role Member -c Projects
!revoke role Moderator -c Staff Channels
```
- Revoking a role from a category disables view, send, connect, speak permissions for all channels in that category.

---

### DELETE COMMANDS

```pgsql
!delete role {role_name}                        
!delete category {category_name}                
!delete channel {channel_name}                  
!delete channel {channel_name} -category {category_name} 
```

### Examples:

```sql
!delete role Member
!delete category Projects
!delete channel general
!delete channel Lobby -category Projects
```

---

### CATEGORY COMMANDS

```pgsql
!create category {category_name}                
!assign role {role_name} -c {category_name}    
!revoke role {role_name} -c {category_name}    
```

---

### CHANNEL COMMANDS

```scss
!create text {channel_name} [-c category_name] 
!create voice {channel_name} [-c category_name]
!delete channel {channel_name} [-category {category_name}] 
```

---

QUICK REFERENCE TABLE

| Command                       | Usage                                                | Description                                    | Example                                    |
| ----------------------------- | ---------------------------------------------------- | ---------------------------------------------- | ------------------------------------------ |
| **Help**                      | `help` or `-h`                                       | Shows available commands                       | `help`                                     |
| **Create Role**               | `!create role {name} [#hex]`                         | Create a role with optional color              | `!create role Member #ff0000`              |
| **Edit Role Name**            | `!edit role {name} name {new_name}`                  | Rename a role                                  | `!edit role Member name NewMember`         |
| **Edit Role Color**           | `!edit role {name} color {#hex}`                     | Change role color                              | `!edit role Moderator color #00ff00`       |
| **Edit Role Permissions**     | `!edit role {name} permission {perm}` or `-p {perm}` | Toggle a permission                            | `!edit role Moderator permission kick`     |
| **Role Shortcut**             | `!edit role {name} set {default/moderator/admin}`    | Apply predefined permissions                   | `!edit role Admin set admin`               |
| **Assign Role to User**       | `!assign {@user} {role_name}`                        | Assign role to user                            | `!assign @John Member`                     |
| **Assign Role to Category**   | `!assign role {role_name} -c {category_name}`        | Grant role access to category                  | `!assign role Member -c Projects`          |
| **Revoke Role from User**     | `!revoke {@user} {role_name}`                        | Remove role from user                          | `!revoke @John Member`                     |
| **Revoke Role from Category** | `!revoke role {role_name} -c {category_name}`        | Remove role access from category               | `!revoke role Member -c Projects`          |
| **Delete Role**               | `!delete role {role_name}`                           | Delete a role                                  | `!delete role Member`                      |
| **Create Category**           | `!create category {name}`                            | Create a category                              | `!create category Projects`                |
| **Delete Category**           | `!delete category {category_name}`                   | Delete a category                              | `!delete category Projects`                |
| **Create Text Channel**       | `!create text {name} [-c {category_name}]`           | Create text channel optionally under category  | `!create text general -c Projects`         |
| **Create Voice Channel**      | `!create voice {name} [-c {category_name}]`          | Create voice channel optionally under category | `!create voice Lobby -c Projects`          |
| **Delete Channel**            | `!delete channel {name} [-category {category_name}]` | Delete channel optionally under category       | `!delete channel Lobby -category Projects` |
