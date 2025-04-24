<h1>Log Analysis Pipeline with ETL, RDS, and Serverless API Integration</h1>

<h2>Description</h2>
In this project, I built an end-to-end data pipeline on AWS by uploading log data to S3, processing it with a Python-based ETL, and storing it in an RDS PostgreSQL database. I created a Lambda function behind an API Gateway (secured with an API key) to provide log statistics (hourly, daily, or weekly). To streamline deployment, I set up CI/CD using GitHub Actions to automatically deploy the Lambda function on every commit.
<br />


<h2>Utilities Used</h2>

- Python
- AWS S3
- AWS RDS (PostgreSQL)
- AWS Lambda
- AWS API Gateway
- boto3, psycopg2, pandas
- GitHub Actions
- pgAdmin

<h2>Project Walk-through</h2>

<h3>Step 1: Upload the Dataset to S3</h3>

<ol>
  <li>Go to <a href="https://www.kaggle.com/code/mahyararani/log-analysis/notebook.-">Kaggle Log Analysis Dataset</a> and download the log file.</li>
  <li>Login to your AWS Console and open the S3 service.</li>
  <li>Create a new bucket and name it.</li>
  <li>Open the bucket > Upload > Add files > Choose your downloaded file > Upload</li>
</ol>

<p align="center">
  <img src="https://i.imgur.com/3ECqYXj.jpeg" alt="S3 Upload Example" width="80%" />
</p>


<h3>Step 2: Create RDS Database with Schema</h3>

<ol>
  <li>Go to AWS Console > RDS > Create database</li>
  <ul>
      <li>Engine: PostgreSQL</li>
      <li>Templates: Free Tier</li>
      <li>DB instance identifier: log-db</li>
      <li>Username: postgres</li>
      <li>Password: StrongPassword</li>
      <li>Enable public access: Yes</li>
      <li>VPC security group: Allow PostgreSQL port 5432</li>
      <li>Create database</li>
    </ul>
  <li>Go to <a href="https://www.postgresql.org/ftp/pgadmin/pgadmin4/v9.2/windows/">postgresql.org</a> and download the .exe file for setting up pgAdmin.</li>
  <li>In pgAdmin, run a query to create the table.</li>
</ol>

<p align="center">
  <img src="https://i.imgur.com/Yr9kETr.jpeg" alt="RDS Example" width="80%" />
</p>


<h3>Step 3: Extract & Load (ETL)</h3>

<ol>
  <li>Launch an EC2 and update it.</li>
  <li>Install boto3, psycopg2, pandas, using pip after enabling python virtual environment.</li>
  <li>Create a script etl_to_rds.py (availble in this repo).</li>
  <li>Run the script.</li>
</ol>

<p align="center">
  <img src="https://i.imgur.com/ndK0MhJ.jpeg" alt="pgAdmin Example" width="80%" />
</p>


<h3>Step 4: Create Lambda Function </h3>

<ol>
  <li>Go to AWS Lambda > Create function.</li>
  <ul>
      <li>Name: your-function-name</li>
      <li>Runtime: Python 3.12</li>
      <li>Role: Create new role with basic Lambda permissions</li>
    </ul>
  <li>Set environment variables (in Lambda console Configuration → Environment variables).</li>
    <ul>
      <li>DB_HOST = your-rds-endpoint</li>
      <li>DB_NAME = your-db-name</li>
      <li>DB_USER = your-db-username</li>
      <li>DB_PASS = YourStrongPassword</li>
    </ul>
  <li>Create a lambda_function.py file (availble in this repo) and install the required library (psycopg2-binary) in the same folder.</li>
  <li>Zip the contents and name it as lambda_deploy.zip.</li>
  <li>Go to AWS Lambda Console → Your Function → Code → Upload from → .zip file → choose lambda_deploy.zip → Deploy</li>
  <li>In Lambda console Test → Configure test { "queryStringParameters": { "period": "hour" } } → event Run and check output.</li>

</ol>
<p align="center">
  <img src="https://i.imgur.com/1XU2l5n.jpeg" alt="Function Example" width="80%" />
</p>


<h3>Step 5: Configure API Gateway with API key </h3>

<ol>
  <li>Search “API Gateway” in AWS search bar → click it.</li>
  <li>Click Create API → Choose HTTP API → Click Build</li>
  <li>Under add integration, choose Lambda and select your function.</li>
  <li>Configure routes → Add route → Method: GET → Resource path: /stats </li>
  <li>Configure stages → Stage name: default (keep default) → Click Create </li>
  <li>Go to API Gateway → Create API Keys</li>
  <li>Go to Usage Plans → Create Usage Plans → Add API stage → Choose your API → Choose the stage (default) → Attach the API Key you created </li>
</ol>

<p align="center">
  <img src="https://i.imgur.com/NVV2Nzm.jpeg" alt="API Gateway Example" width="80%" />
</p>


<h3>Step 6: Set Up CI/CD with GitHub Actions</h3>

<ol>
  <li>Create GitHub Repo.</li>
  <li>Push your lambda_function.py, lambda_deploy.zip, and requirements.txt file to this repo.</li>
  <li>Create GitHub Actions Workflow file (.github/workflows/deploy.yml).</li>
  <li>In your repo, Go to Settings > Secrets and variables > Actions > New repository secret.</li>
  <li> Add these two secrets: AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY</li>
</ol>

<p align="center">
  <img src="https://i.imgur.com/0UnnbJs.jpeg" alt="CI/CD with GitHub Actions Example" width="80%" />
</p>

