# Tower Export

This role exports the conf_setting table from the awx database. It also exports all standard content objects from tower. It will not export encrypted content objects. It is designed for disconnected environment.

## Dependencies

In order to use this module tower-cli must be installed on the host executing this role.

This role expects python2 to be installed to install psycopg2 package.

## Variables

### Mandatory
- `tower_admin`
	- *Example:* admin
- `tower_password`
  - *Example:* password
- `working_path`
  - *Example:* /home/test
- `postgres_password`
  - *Example:* password
- `postgres_host`
  - *Example:* 127.0.0.1

### Gitlab Vars
- `None`

## Role Variables

| Variable   | Comments (type)  |
| :---       | :---             |
| `tower_admin` | String - Name of admin account |
| `tower_password` | String - password |
| `working_path` | String - path where tower-cli.cfg will be placed |
| `postgres_password` | String - password |
| `postgres_host` | String - ip address of postgres server |



## Environment Variables

| Variable   | Default | Comments (type)  |
| :---       | :---    | :---             |
| `none` | None  | None |
