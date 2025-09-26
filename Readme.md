# Discord bot
### Under development

## HELP

```bash
help -h - soon

!create -h -soon
```

## CREATE
```
!create
        role {name}
        category {name}
        text (channel) {name}
        voice (channel) {name}
```

## ROLE

```css !create role {name}

!create role {name} {#color_hex}

!edit role {name} name {new_name}

!edit role {name}
                permission {permission_name}
                -p {permission_name}

```

### List of permissions:
```bash
    perm_aliases = {
        "kick": "kick_members",
        "ban": "ban_members",
        "manage": "manage_messages",
        "admin": "administrator",
        "mention": "mentionable",
        "hoist": "hoist",
        "manage_roles": "manage_roles",
        "manage_channels": "manage_channels",
        "read": "read_messages",
        "send": "send_messages",
        "embed": "embed_links",
        "attach": "attach_files",
        "voice": "connect",
        "speak": "speak",
        "mute": "mute_members",
        "deafen": "deafen_members",
        "move": "move_members",
        "priority": "priority_speaker"
    }
```

```shell
!assign {@user} {role_name}

!revoke {@user} {role_name}

!delete role {role_name}
!delete {role_name} - for now
```

## CATEGORY

!create category {name}

## CHANNEL

!create channel {name}