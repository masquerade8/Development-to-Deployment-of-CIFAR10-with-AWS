# Development to-Deployment-of-CIFAR10-with-AWS
Build a pipeline (development to deployment) involving any DL model for any specific downstream task in AWS. Also provide a web interface to use this deployed model. What are the different ways of deployment in AWS?


Machine and Deep Learning Deployment Project on AWS

This README provides a step-by-step guide to deploy a machine and deep learning model on AWS using S3, SageMaker, and EC2 with Flask to create a web app.

Prerequisites
- Basic understanding of AWS services (S3, SageMaker, EC2).
- An Amazon Free Tier account.
- Familiarity with Python and Flask for web applications.

Step 1: Set up an AWS Free Tier Account
1. Go to the AWS Free Tier page: https://aws.amazon.com/free/.
2. Sign up for a new account by following the instructions.

Step 2: Set up an S3 Bucket
1. Go to the S3 service in the AWS console.
2. Create S3 Bucket:
   - Enter a unique name for your S3 bucket.
   - Enable ACLs.
   - Uncheck "Block all public access".
   - Leave other settings as default.
3. Click Create bucket.

Step 3: Create and Configure a SageMaker Notebook
1. Open the SageMaker service in the AWS console.
2. Notebook Setup:
   - Select Notebook from the left-hand breadcrumb.
   - Click Create Notebook Instance.
3. Notebook Instance Configuration:
   - Choose the instance type (We are suggesting to use ml.m5.xlarge which will cost you around $0.23/hour).
   - Create a new IAM role with access to your S3 bucket.
4. Start and Open Jupyter Notebook:
   - Start the notebook instance and open Jupyter Notebook.
   - Create a new file, and select the kernel (conda_tensorflow2_p310 in this case).
5. Write and Run SageMaker Code:
   - Implement your SageMaker code to train and deploy the model, saving the trained model to the S3 bucket created in Step 2.

Step 4: Create and Configure an EC2 Instance
1. EC2 Setup:
   - Go to the EC2 service in the AWS console.
   - Create a new EC2 instance:
     - Name the instance.
     - Select Ubuntu as the OS image (free tier eligible).
     - Create a new key pair (leave default settings).
   - In Network settings, check all three "Allow traffic" boxes.
   - Click Launch Instance.
2. Configure IAM Role for EC2:
   - Go to Instances -> Actions -> Security -> Modify IAM Role.
   - Create a new role with:
     - Use case: EC2.
     - Permission policies: Search and select AmazonS3FullAccess.
   - Name and create the role.
   - Go back to EC2 -> Actions -> Security -> Modify IAM Role, find and attach the created role.
3. Connect to the EC2 Instance:
   - Select Connect from the EC2 dashboard.
   - Use EC2 Instance Connect to access the terminal.

Step 5: Set Up the EC2 Environment for the Web App
1. Update and Install Python:
   sudo apt-get update
   sudo apt install python3.12-venv

2. Set Up Project Directory and Virtual Environment:
   mkdir <project-directory-name>
   cd <project-directory-name>
   python3 -m venv myenv
   source myenv/bin/activate

3. Install Required Packages:
   pip install flask tensorflow pillow boto3

4. Create Flask App:
   - Create app.py to handle model loading and predictions:
     sudo nano app.py
   - Include Flask code that:
     - Loads the model from the S3 bucket to the EC2 instance.
     - Uses the model to make predictions.

5. Set Up HTML Template Directory:
   - Create the template directory and index.html:
     mkdir templates
     sudo nano templates/index.html

6. Configure Security Groups:
   - Go back to EC2 Instances -> Security Groups.
   - Edit Inbound and Outbound Rules:(For outbound you have to delete the existing rule)
     - Set Type to "All Traffic".
     - Set Source to "Anywhere - IPv4".

Step 6: Run the Flask Web App
1. Run the Flask app:
   python3 app.py

2. Access the Application:
   - In EC2 Instances -> Connect -> SSH Client, copy the Public DNS.
   - Paste the DNS in a browser with the correct port if needed (e.g., http://<public-dns>:5000).

Notes
- Make sure to stop all the services of the AWS before closing it either it will cost you a lot.
- Ensure all settings match your project's requirements.
- Verify permissions on S3 and EC2 for access control.

This guide provides a comprehensive setup for deploying a machine and deep learning model as a web application on AWS using Flask, S3, SageMaker, and EC2.

