# Deployment

A box of scripts designed to drop next to the deployment, and help to script
configure  deploy the app from a single source.

1. All required scripts
2. Checklist deployment
3. Automated tools

And a config for the outbound solution.


Working examples:

Start a project from a repo:

  tpd start git@github.com:Strangemother/polypoint.git

Load a project from a directory, reading its fresh config

  tpd start C:\Users\jay\Documents\projects\polypoint

---

## WIP

---

    deploy start git://name.git
    # look for name/
        # error out
    # clone
        # look for pocket.json


    deploy start pocket.json


    deploy start .
    # Look for pocket.json


The config contains the info to execute the processes.

    {
        name: "app-name" # the git name
        path: . # default _current_ or _src_
        git: 'git...'
        branch: 'HEAD'
    }


once collected start can proceed.

---

It's acceptable to apply the `pocket.json` within the `deployment` folder.
However anywhere should be acceptable.

---

# Git-Based Deployment Flow

This outlines a streamlined deployment process using a minimal config and Git integration.

---

## 1. Initialize Deployment

- Start with a command that accepts:
  - A minimal config file
  - A Git URL
  - Or a local path

## 2. Clone or Update Repository

- **If Git URL provided:**
  → Clone repository to the specified deployment directory.

- **If directory already exists:**
  → Run `git pull` to update the code.

## 3. Load Full Configuration

- After pulling/cloning, read the **full config file** from the repository.
- This config includes:
  - Environment variables
  - Deployment paths
  - Custom instructions

## 4. Execute Deployment Steps

- Install dependencies
- Set environment variables
- Run any service hooks (e.g., reload/restart)
- Apply any config-specific setup

## 5. Final Verification

- Check for:
  - Errors in the deployment process
  - Service uptime
  - Correct versions running
- Log output for reference

---

> Tip: Consider using a wrapper script (`deploy start`) to abstract these steps for ease of use.
