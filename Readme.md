# Portfolio Website CI/CD Deployment on AWS EC2 using Docker and Jenkins

This document outlines the step-by-step implementation of a complete CI/CD pipeline to deploy a portfolio website using git&github, Docker, Jenkins, and AWS EC2. It also includes key tools used, real-world issues encountered, and their respective solutions.

## Tools and Technologies Used

- AWS EC2 instance (Ubuntu)
- Docker and DockerHub
- Jenkins (installed locally on Windows)
- ESlint for testing javascript code and potential issues.
- Git (version control)
- GitHub (as the source code repository)
- LocalTunnel (to expose Jenkins to the internet for GitHub webhook)
- Gmail SMTP (to send build notifications)
- Windows Task Scheduler (to automate Jenkins backup)

## Project Workflow

1. **EC2 Instance Setup**

   - A free-tier Amazon Linux EC2 instance was launched from AWS with a `.pem` key.
   - File permission was changed using: `chmod 400 key.pem`
   - SSH connection was established using:
     ```
     <!-- (important info is not shown for security purposes) -->
     ssh -i key.pem ec2-user@your-ec2-ip  
     ```

2. **Correcting Case-Sensitive File Issue**

   - The file was named `Index.html`, but Linux is case-sensitive and expected `index.html`.
   - Fixed using the following Git commands:
     ```
     <!-- A new file temp.html was used to make the version control and github detect the change  -->
     git mv Index.html temp.html
     git commit -m "rename to temp"
     git mv temp.html index.html
     git commit -m "final rename"
     git push
     ```

3. **Docker Image Creation and Push to DockerHub**

   - After building the image locally, it was tagged and pushed using:
     ```
     docker tag my-portfolio:latest shivam8168/myportfolioimage:my-portfolio
     docker push shivam8168/myportfolioimage:my-portfolio
     ```

4. **Pull and Run Docker Image on EC2**

   - Commands used:
     ```
     sudo docker pull shivam8168/myportfolioimage:my-portfolio
     sudo docker run -d -p 80:80 shivam8168/myportfolioimage:my-portfolio
     ```

5. **Jenkins Setup on Local Windows Machine**

   - Jenkins was installed locally.
   - Required plugins were added including Git, Docker Pipeline, SSH Agent, and Pipeline plugins.
   - Credentials were created in Jenkins:
     - DockerHub username and PAT
     - EC2 SSH private key
     - GitHub PAT (PAT expires , so need to update again)

6. **GitHub Webhook Integration**

   - GitHub was configured to notify Jenkins via webhook when changes are pushed.
   - Jenkins was exposed to the internet using `localtunnel`:
     ```
     npx localtunnel --port 8080 --subdomain shivamjenkins8168
     ```
     above command help to create a tunnel port that expose jenkins through a URL
   - A `.bat` file was created to start the tunnel easily:
     ```
     @echo off
     lt --port 8080 --subdomain shivamjenkins8168
     pause
     ```

7. **Jenkins Pipeline Job (Windows-Friendly)**
   

   - A declarative pipeline was created using `bat` steps instead of `sh` since it runs on Windows.
   - The stages include:
     - Cloning the GitHub repository
     - testing the code using ESlint
     - Building and pushing the Docker image
     - SSH into EC2 and pulling the new image
     - Stopping old container (if any) and running the new one

8. **Email Notification for Build Failures**

   - Jenkins was configured with Gmail SMTP to send alerts:
     - SMTP: smtp.gmail.com
     - Port: 465
     - SSL: Enabled
     - Authentication via App Passwords (from Google Account)
   - Recipient list was added to notify stakeholders on build failures.

9. **Automated Jenkins Backup**

   - Windows Task Scheduler was used to take periodic backup of the `.jenkins` directory.
   - Backup folder was synced to Google Drive for cloud safety.

## Common Errors Faced and Fixes

1. **Index.html not served**

   - Cause: File was named `Index.html`, but Linux is case-sensitive.
   - Solution: Rename using Git commands as outlined above.

2. **IOException when using 'sh'**

   - Cause: Jenkins on Windows does not support `sh`.
   - Solution: Use `bat` instead of `sh` in pipeline scripts.

3. **Docker login failed using environment variables**

   - Cause: Incorrect environment variable syntax.
   - Solution: Use `%VARIABLE_NAME%` for Windows instead of `$VARIABLE_NAME`.

4. **Webhook returning HTTP 403**

   - Cause: Jenkins CSRF protection and anonymous access blocked.
   - Solution: Allowed anonymous users to have read and build permissions in Jenkins security matrix.

5. **StringIndexOutOfBoundsException**

   - Cause: Missing SSH credentials or improperly passed environment variables.
   - Solution: Validate that all credentials and variables are correctly configured.

6. **Tunnel expired or showing '503'**

   - Cause: Tunnel timed out or closed.
   - Solution: Reopen tunnel using the `.bat` script and avoid sleeping or restarting the system.
   - Also keep the terminal open duRing triggering(pushing code changes).

7. ** ESLint not recognized ScrollReveal and Typed function**
   - cause: Eslint do not recognized the if the function or variable is used in external file.
   - Solution: Add the below comment on top of script.js to make Eslint understand it as global.
   -  /* global Typed, ScrollReveal */
   

###  Some Good pracTices I considered:
   - Local Installation:
     Installed Jenkins locally not on EC2 instance to avoid high use of EC2 resources.
    the tool LocalTunnel helped me to use Jenkins in professional manner.

   - Email Notification:
     Configured and utilized Email Notification service to get build information quickly whether build is successful or not so that instant action can be taken.

    - Budget and Alarms:
      Setted up budget and alarms on AWS so that I can avoid charges and remain within the free-tier.

    - Lambda function:
      Python is used to to create a lambda function using boto3, lambda function is triggered by cloudwatch to stop the running EC2 instance after sending email notification.  

    - Backup:
     As Jenkins is locally installed, I used a script that backups my jobs and important files to drive.

    - Task Scheduler:
     Windows task Scheduler is used to run the script on a particular time that backups all important jobs, configuration files everyday.

## Summary

This project successfully demonstrates a complete CI/CD setup to deploy a portfolio website with real-time GitHub webhook integration, Docker-based deployment on an EC2 instance, and Jenkins automation. Common challenges encountered during this process were resolved with targeted solutions. The system is also equipped with email alerts and regular backups, making it production-ready and reliable for continuous deployment workflows.

# Live Links
- Live from EC2(project):
   http://35.175.145.107/

- Alternate Portfolio Link:
   https://shivam8168.netlify.app/  

- Project Readme (Also available on portfolio)
   https://github.com/ShivamSharma8168/CICD_Portfolio_Readme   

## Note

This project is done to gain hands-on experience on DevOps concepts at beginner level.
All the resources used are free and also due to AWS Free-Tier account.
I am currently working on it and take it another level to experience real Devops practices.
 