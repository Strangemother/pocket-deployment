https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu

Install the Packages from the Ubuntu Repositories
Creating the PostgreSQL Database and User
Create a Python Virtual Environment for Project
Create and Configure New Django Project
Complete Django Project Setup
Test Gunicorn’s Ability to Serve the Project
Creating Gunicorn systemd Socket and Service Files
Check Gunicorn Socket File
Testing Socket Activation
Configure Nginx to Proxy Pass to Gunicorn
Troubleshooting Nginx and Gunicorn


clone project                   # first time
checkout target branch          # every time
    and PULL
ensure venv
    install venv dependencies


---

# Actual

## Generate box (with SSH enabled)

create instance ensuring SSH, gather the IP

## Add Key

If the key is not automatically applied, add a key
A login to the _target_ is required. Maybe as _root_


1. On the _client_ perform `ssh-keygen`
2. Store the key locally for convenience
3. On the _target_, add the `.pub` content to `.ssh/authorized_keys`

we'll name the `id_rsa` as `new_key`

## Connect

    ssh root@1.2.3.4 -i new_key
    ~# |


## New (Site) User

Generate new user specific for this deployed work, and password automatically:

```bash
NEW_USERNAME=site_user
NEW_PASSWORD=$(python3 -c 'import crypt; print(crypt.crypt("fridgeM4gnet"))')
useradd -m -p $NEW_PASSWORD -s /bin/bash $NEW_USERNAME
# wipe
NEW_PASSWORD=
usermod -aG sudo $NEW_USERNAME
```

lock a user: (to prevent login and other securities)
However this will block login...

```bash
usermod --lock <username>
```


## Update box

This can be done under the new user (e.g. `site_user`)

    sudo apt-get update
    sudo apt-get install python3-pip python3-venv -yq

## Generate key

```bash
NEW_KEYFILENAME="site_user_keyfile"
NEW_USERNAME="site_user"

ssh-keygen -m PEM -t rsa -b 2048 -f site_user_keyfile -N "" -C "legacy@friendly"
cp ${NEW_KEYFILENAME}.pub  /home/${NEW_USERNAME}/.ssh/id_rsa.pub
tee -a /home/${NEW_USERNAME}/.ssh/authorized_keys < ${NEW_KEYFILENAME}.pub
cp ${NEW_KEYFILENAME} /home/${NEW_USERNAME}/.ssh/id_rsa
cat ${NEW_KEYFILENAME}
```

Copy the content into the local `site_user_key`

```bash
ssh site_user@104.248.173.241 -i  site_user_key
```

---

