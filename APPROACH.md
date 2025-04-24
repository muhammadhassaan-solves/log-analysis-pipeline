# Approach and Decisions    

### What this task is about   
The objective is to build a simple and scalable log analysis pipeline using AWS services with CI/CD. 
This system is designed to store raw log data, process it for analysis, and expose an API to query the processed data for insights.

### Technologies Used  

| Component    | Tool                    | Reason                               |
|--------------|-------------------------|--------------------------------------|
| Storage      | S3                      | To store raw log file                |
| Processing   | EC2 + Python (ETL)      | Easy for scripting and flexibility   |
| Database     | RDS (PostgreSQL)        | Best fit for structured log data     |
| API Access   | Lambda + API Gateway    | Serverless and cost-effective        |
| Automation   | GitHub Actions          | CI/CD for auto deployment            |

### Workflow  

1. Upload log file to S3.  
2. EC2 runs Python ETL to transform and load logs into RDS.  
3. Lambda queries RDS and returns counts (hourly, daily, weekly).  
4. API Gateway exposes Lambda (with API Key protection).  
5. GitHub Actions deploys Lambda on new commits . 


### Security & Best Practices  

- Used environment variables for secrets  
- Lambda packaged with dependencies  
- API secured using API Key  
- Code and infra in version control  

### Prompts Used with LLM  

These prompts helped me complete the task step-by-step as a beginner:

**Prompt 1**  
>You are data and infrastructure engineer. Being an absolute beginner, help me perform it according to the provided instructions in the copy-paste format.  
>(Shared the same full task description with LLM to break it down simply, excluding email address)

**Prompt 2**  
>Help me understand what I am supposed to do.  
>(Shared the same full task description with LLM to break it down simply, excluding email address)
