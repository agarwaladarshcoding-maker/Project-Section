import csv
import random
import os

# Set random seed for reproducibility
random.seed(42)

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
OUTPUT_FILE = os.path.join(DATA_DIR, 'training_data.csv')

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)

TOOLS = [
    "ChatGPT", 
    "Claude.ai", 
    "Antigravity browser", 
    "Antigravity Mac app", 
    "Ollama CLI", 
    "Claude Code CLI", 
    "VS Code Cline"
]

COMPONENTS = [
    "auth module", "database schema", "UI layout", "API endpoint", 
    "Redis cache", "Docker container", "login component", 
    "payment gateway", "unit tests", "cron job", "background worker",
    "payment integration", "search index"
]

# Provide exactly 40 short templates per category.
EVENT_TYPES = {
    "ERROR": {
        "templates": [
            "Unhandled exception in {component}: Connection refused.",
            "Agent process crashed unexpectedly while working on {component}. Exit code 1.",
            "Failed to compile {component}. SyntaxError at line 42.",
            "Out of memory error when processing {component}.",
            "Error: could not resolve dependencies for {component}.",
            "Fatal error: API key missing for {component}.",
            "Traceback (most recent call last): Exception in {component}.",
            "The build failed for {component}. See logs for details.",
            "Command 'npm install' failed in {component} folder.",
            "Encountered a critical bug in {component} preventing further execution.",
            "ECONNRESET: failed to establish connection to {component}.",
            "Database lock timeout exceeded in {component}.",
            "Null reference exception discovered during the execution of {component}.",
            "Segmentation fault (core dumped) when parsing {component}.",
            "Unable to write to output directory for {component}.",
            "Network unreachable error thrown by {component} module.",
            "Authentication failed when trying to access {component}.",
            "JSON decoding error: malformed data received by {component}.",
            "The execution environment for {component} lacks required permissions.",
            "Timeout exception: {component} failed to respond within 30000ms.",
            "Syntax parsing failure in {component}: unexpected token.",
            "Missing required configuration parameter within {component} setup.",
            "A severe application fault occurred in the {component} subsystem.",
            "Execution aborted: {component} returned an unrecognized error code (-9).",
            "Failed to allocate necessary heap space for {component}.",
            "Invalid API response structure from {component} server.",
            "The operating system forcibly closed the connection for {component}.",
            "Worker thread for {component} died unexpectedly.",
            "Import error: module not found while initializing {component}.",
            "An unknown error halted the process dealing with {component}.",
            "Deadlock detected in {component} database transaction.",
            "Could not initialize {component}. Disk space full.",
            "Internal server error 500 received while calling {component}.",
            "Module {component} threw an unrecoverable runtime exception.",
            "Validation of existing schemas failed in {component}.",
            "Agent kernel panic. The context state for {component} was lost.",
            "Corrupted payload detected. Failed to process {component}.",
            "A stack overflow occurred inside {component} recursive call.",
            "Failed to spawn child process for {component} worker.",
            "I hit a major roadblock. My internal logic crashed reading {component}."
        ],
        "ui_contexts": ["Critical Error", "Process Failed", "Exception", "Terminal Output", "Agent Error", "Execution Halted", "Stderr Output"],
        "buttons": ["View Logs,Retry,Dismiss", "Show Error,Dismiss", "Restart Agent,View Traceback", "Retry", "View Details,Cancel", "Debug,Retry,Ignore"],
        "allow_empty_buttons": True
    },
    "BLOCKED": {
        "templates": [
            "Waiting for human verification to proceed with {component}.",
            "Encountered a CAPTCHA while scraping {component}. Please solve it.",
            "Paused for manual 2FA entry for {component}.",
            "Stuck at SSH password prompt while connecting to {component}.",
            "Testing framework paused. Please inspect the DOM in {component}.",
            "Interactive prompt detected in {component}. Waiting for input.",
            "Cannot bypass the security check for {component}. Manual intervention required.",
            "Agent execution suspended. Awaiting human confirmation for {component}.",
            "Login flow blocked by SMS verification challenge for {component}.",
            "Operation stalled. Please accept the terms of service manually for {component}.",
            "I am halted. Please fix the external {component} validation before we can continue.",
            "Awaiting email confirmation link click for {component}. Please do this.",
            "The {component} service wants you to answer a security question.",
            "I'm paused. Insert the hardware security key to unblock {component}.",
            "Cannot proceed. A manual signature is required to finalize {component}.",
            "The web interface for {component} presented a puzzle. Solve it to unblock me.",
            "Browser verification page detected while evaluating {component}. I can't read it.",
            "A modal dialog requires a manual click to resume {component}.",
            "Please input the 6-digit authenticator code for {component}.",
            "Stuck at an OAuth consent screen for {component}. Click accept.",
            "Blocked by a cloud firewall challenge. Confirm you are human for {component}.",
            "Waiting for you to log into the VPN before accessing {component}.",
            "I am stuck at a 'Choose your account' screen in {component}.",
            "Execution frozen. External manual approval is needed to start {component}.",
            "The SSH key requires a passphrase. Please type it in for {component}.",
            "A manual device authorization is required for {component}. Waiting.",
            "Pushed a notification to your phone. Approve it to unblock {component}.",
            "Locked behind a pin code entry screen on {component}.",
            "I've hit a paywall popup on {component}. Can't continue.",
            "The {component} CLI is waiting for interactive standard input.",
            "Blocked state. Please close the conflicting application using {component}.",
            "Waiting. Ensure the external hardware for {component} is plugged in.",
            "Paused. You need to manually drag and drop the file into {component}.",
            "There's a terms and conditions scroll wall on {component} blocking me.",
            "I cannot access {component} until the local network proxy is authenticated.",
            "Execution suspended. The {component} server is in maintenance mode.",
            "Stuck. A password expiration prompt appeared for {component}.",
            "A mandatory survey popup appeared on {component}. Dismiss it so I can work.",
            "Awaiting biometric verification (Touch ID / Face ID) from the system for {component}.",
            "I detected a locked screen status while trying to automate {component}."
        ],
        "ui_contexts": ["Action Required", "Agent Blocked", "Input Needed", "Status: Blocked", "Wait State", "Verification"],
        "buttons": ["View,Unblock,Dismiss", "Solve CAPTCHA,Skip", "Enter Passcode,Cancel", "Proceed manually", "Resume,Abort", "Provide Input,Cancel"],
        "allow_empty_buttons": False
    },
    "PERMISSION": {
        "templates": [
            "I need to execute a command to delete {component}. Proceed?",
            "Do you want me to replace the existing {component} with the new implementation?",
            "Requesting permission to modify production {component}.",
            "Shall I commit and push these changes to {component}?",
            "About to run a destructive script on {component}. Do you approve?",
            "Can I apply the database migration for {component}?",
            "I am ready to deploy {component}. Should I go ahead?",
            "Do you allow the agent to read local files in {component}?",
            "Need authorization to restart {component}. OK?",
            "Permission requested to overwrite {component}.",
            "I've prepared a PR for {component}. Do I have the green light to open it?",
            "Shall I proceed to permanently drop the table in {component}?",
            "Can I reformat the entire codebase inside {component}?",
            "Do you approve merging this branch into main for {component}?",
            "I want to install new global system dependencies for {component}. Allow?",
            "Is it OK if I publish the {component} package to the registry now?",
            "I need elevated sudo privileges to configure {component}. Approve?",
            "May I clear the production cache for {component}?",
            "Confirm you want me to spin up 50 new instances of {component}.",
            "Do I have the authorization to change the firewall rules for {component}?",
            "I'm about to send automated emails using {component}. Confirmed?",
            "Can I forcefully terminate the hanging process in {component}?",
            "Would you like me to push this hotfix for {component} live?",
            "I plan to rewrite git history for {component}. Is this acceptable?",
            "Allow me to update the secret keys for {component}?",
            "Shall I run the wipe script across {component}?",
            "Do you want me to automatically fix all lint errors in {component}?",
            "I am requesting access to read your private keys for {component}.",
            "Is it safe to drop and recreate the {component} database?",
            "Approve the new API usage charges estimated for {component}?",
            "Ready to rollback {component} to the previous version. Proceed?",
            "Should I bypass the safety checks to execute {component}?",
            "Can I format the secondary drive for {component}?",
            "May I upload the local source files of {component} to the cloud?",
            "I will overwrite your local unsaved changes in {component}. OK?",
            "Confirm deletion of all archived logs in {component}.",
            "Do you grant permission for the agent to share {component} publicly?",
            "Shall I run the stress test on {component} right now?",
            "Is it alright if I close out all open issues tagged with {component}?",
            "I need your go-ahead before mutating {component} state."
        ],
        "ui_contexts": ["Permission Request", "Approval Needed", "Confirmation", "Terminal Prompt", "Action Authorization", "Security Check"],
        "buttons": ["Allow,Deny", "Proceed,Cancel,Show Plan", "Yes,No", "Run Command,Edit Command,Cancel", "Approve,Reject", "Authorize,Decline", "Approve Execution,Cancel"],
        "allow_empty_buttons": False
    },
    "LIMIT": {
        "templates": [
            "Rate limit exceeded for {component} API. Backing off for 60 seconds.",
            "Daily token quota reached while generating {component}.",
            "Context window limit reached in {component}. Please summarize.",
            "You have hit the maximum request limit for {component}.",
            "API usage capped out for {component}.",
            "Too many requests to {component}. Please try again later.",
            "Token limit warning: {component} requires more tokens than available.",
            "Resource exhausted allocating {component}.",
            "Billing limit reached. Cannot scale up {component}.",
            "Query complexity limit exceeded for {component}.",
            "We are approaching the allowed spending cap for {component}.",
            "The {component} agent is currently throttled due to excessive usage.",
            "Maximum concurrent sessions limit reached. {component} request dropped.",
            "Storage quota limit exceeded. Cannot save {component} logs.",
            "You've exceeded the free tier limitations for {component}.",
            "The context length is too long to process {component}. Truncation needed.",
            "Insufficient credit balance to run inference on {component}.",
            "Hard usage cap reached on the OpenAI model for {component}.",
            "API throughput limits hit on {component} database.",
            "Cannot allocate more CPUs. The compute limit is saturated by {component}.",
            "Your IP has been temporarily rate-limited when accessing {component}.",
            "You hit the daily API call allowance for the {component} integration.",
            "Maximum output length reached while rendering {component}.",
            "Monthly budget exceeded for cloud operations on {component}.",
            "Agent is paused due to token exhaustion during {component} code generation.",
            "The endpoint for {component} returned a 429 Too Many Requests status.",
            "File size exceeds the maximum upload limit for {component}.",
            "Exceeded the 5-minute timeout limit for compiling {component}.",
            "Workspace storage is at 100% capacity. Cannot write {component}.",
            "Subscription tier does not support the requested scale of {component}.",
            "You have hit the model context limit of 128k tokens for {component}.",
            "The max_depth limit was exceeded parsing the recursive {component}.",
            "Network bandwidth usage has been capped for {component}.",
            "System thread limit reached. Cannot spawn new worker for {component}.",
            "You are restricted to 100 queries per hour for {component}.",
            "The generated code was truncated because it exceeded {component}'s token limits.",
            "Reached the max iterations limit solving the logic for {component}.",
            "API key has surpassed its hard limit threshold for {component}.",
            "Limit violation: the request size for {component} is too large.",
            "I cannot process {component} because you ran out of daily credits."
        ],
        "ui_contexts": ["Quota Exceeded", "Rate Limit Status", "Warning", "Usage Alert", "API Limit", "Billing Notice"],
        "buttons": ["View,Dismiss", "Upgrade Plan,Dismiss", "Wait,Cancel", "Manage Quota", "Acknowledge", "Check Usage,Dismiss"],
        "allow_empty_buttons": False
    },
    "DECISION": {
        "templates": [
            "How should I handle the timeout scenario in {component}?",
            "Which framework do you prefer for {component}: React or Vue?",
            "I found multiple matches for {component}. Which one should I select?",
            "Should we implement {component} now or defer it to Phase 2?",
            "What is the expected behavior when {component} fails?",
            "Please clarify the requirements for {component}.",
            "Do you want pagination on {component} or infinite scroll?",
            "I can use MongoDB or PostgreSQL for {component}. Thoughts?",
            "Should {component} be accessible to guest users?",
            "How do you want to handle error logging for {component}?",
            "They both have tradeoffs. Should I prioritize speed or memory for {component}?",
            "What color scheme should I apply to the new {component}?",
            "I can write this {component} in Python or Node. Which do you prefer?",
            "Which branching strategy should I use when committing {component}?",
            "Can you provide the exact text you want displayed on the {component}?",
            "I'm unsure about the logic in {component}. Should I guess or ask the user?",
            "What port number do you want to expose for {component}?",
            "Do you want to use strict type checking for the {component} code?",
            "Should I focus on unit tests or e2e tests for {component} today?",
            "Which version of the SDK should I install for {component}?",
            "Do you want me to mock the database responses for {component}?",
            "Where should I store the output reports generated by {component}?",
            "Should {component} use synchronous or asynchronous processing?",
            "Can you clarify the edge case where the user has no permissions in {component}?",
            "Do we need backward compatibility for the legacy {component}?",
            "I see a conflict in {component}. Keep your version or incoming changes?",
            "Do you want {component} to be deployed as a lambda or a container?",
            "Which authentication method will {component} primarily rely on?",
            "Should the {component} default to dark mode or light mode?",
            "What format do you want the exported data from {component} to be in?",
            "Is the intended audience for {component} internal or external?",
            "Should I ignore node_modules when analyzing {component}?",
            "Which CSS library should we integrate into {component}?",
            "What URL path should route to the {component}?",
            "How many retry attempts should I configure for {component}?",
            "Do you want to use the default settings or custom configurations for {component}?",
            "Should the {component} be tightly coupled or decoupled from the main app?",
            "What specific metrics should we be tracking in {component}?",
            "Should the placeholder text for {component} be funny or professional?",
            "I can implement {component} using a library or from scratch. What is better?"
        ],
        "ui_contexts": ["Question", "Agent Query", "Decision Needed", "Awaiting Input", "Clarification Required", "Prompt"],
        "buttons": ["Reply", "Answer", "Provide Input", "Submit Answer,Cancel", "Respond", "Reply,Skip"],
        "allow_empty_buttons": False
    },
    "RECOMMEND": {
        "templates": [
            "I noticed {component} could be optimized using memoization.",
            "Warning: The library used in {component} is deprecated.",
            "It looks like {component} is missing unit tests. Consider adding them.",
            "Suggestion: we might want to refactor {component} since it's getting large.",
            "Found a potential security vulnerability in {component}. Not blocking.",
            "You could simplify the logic in {component} by using a switch statement.",
            "Recommendation: update dependencies for {component}.",
            "Code smell detected in {component}: high cyclomatic complexity.",
            "Consider caching the results of {component} to improve performance.",
            "Tip: {component} can be deployed serverless for lower costs.",
            "By the way, there's a more efficient built-in method for {component}.",
            "A minor optimization: you could avoid the nested loop in {component}.",
            "I suggest enabling strict mode for the {component} going forward.",
            "You might want to extract {component} into its own separate microservice.",
            "Note that your implementation of {component} is not fully accessible.",
            "I recommend adding a debounce function to the inputs in {component}.",
            "Just an observation: {component} could benefit from lazy loading.",
            "Consider upgrading {component}'s base image to the latest Alpine version.",
            "The naming convention in {component} is slightly inconsistent; consider fixing it.",
            "You should probably add proper logging to {component}.",
            "I've noticed {component} sometimes fails silently. Consider adding a try/catch.",
            "It's generally a best practice to keep {component} stateless.",
            "There is a simpler open-source alternative you could use for {component}.",
            "A quick tip: the CSS in {component} might break on Safari.",
            "Consider sanitizing the inputs in {component} to prevent XSS.",
            "The layout for {component} would look much cleaner with flexbox.",
            "I advise migrating {component} to TypeScript for better type safety.",
            "You could arguably write {component} with 50% fewer lines of code.",
            "Heads up: {component} relies on an unmaintained npm package.",
            "I highly recommend caching the API responses in {component}.",
            "You might face scaling issues with the current architecture of {component}.",
            "It would make sense to use environment variables instead of hardcoding {component}.",
            "Consider adjusting the timeout settings on {component} to be higher.",
            "You might want to add rate limiting to {component} to prevent abuse.",
            "An index on the database column would vastly speed up {component} queries.",
            "Just a visual critique: {component} lacks enough contrast for readability.",
            "I suggest using a linter on {component} before merging it.",
            "A small suggestion: {component} 's error messages could be more user-friendly.",
            "Consider setting up a CI/CD pipeline to automate deployments of {component}.",
            "Adding pagination to {component} will prevent it from loading too slowly."
        ],
        "ui_contexts": ["Suggestion", "Optimization", "Warning", "Analysis Complete", "Linter Output", "Best Practice"],
        "buttons": ["View,Dismiss", "Ignore,View Suggestions", "Dismiss", "Read More", "Review Recommendation,Skip", "Apply,Dismiss"],
        "allow_empty_buttons": True
    },
    "COMPLETED": {
        "templates": [
            "Successfully deployed {component} to production.",
            "Finished refactoring {component}.",
            "All tests passed for {component}. Task complete.",
            "I've completed the {component} implementation as requested.",
            "Done writing the documentation for {component}.",
            "The script for {component} finished running successfully.",
            "Data migration for {component} is 100% complete.",
            "Resolved the bug in {component}.",
            "Code execution for {component} finished with code 0.",
            "{component} setup is done and ready to use.",
            "The changes to {component} are published and live.",
            "All requested modifications to {component} have been applied successfully.",
            "Automated build sequence for {component} finished without errors.",
            "I wrapped up the unit tests for {component}. Coverage is good.",
            "The new database schema for {component} has been successfully provisioned.",
            "I finish exploring the codebase. {component} research is complete.",
            "The pull request containing {component} has been successfully merged.",
            "Done. I've exported the raw data for {component} into the designated folder.",
            "The system health check for {component} completely passed.",
            "Code cleanup for {component} executed to perfection.",
            "The {component} instance is now running smoothly in the background.",
            "Package installation for {component} completed successfully.",
            "Image assets for {component} have all been successfully optimized.",
            "I have entirely finished analyzing the logs for {component}.",
            "The security audit for {component} is finished.",
            "The CI/CD pipeline triggered by {component} has succeeded.",
            "Success! I got the prototype for {component} fully working.",
            "Finished converting {component} line by line to proper syntax.",
            "I've thoroughly checked {component}. Everything is ready to go.",
            "Data ingestion pipeline for {component} has finished its batch run.",
            "Creation of the initial repository for {component} is done.",
            "The background worker compiling {component} terminated successfully.",
            "SSL certificates for {component} were renewed perfectly.",
            "Docker image build for {component} completed in 32 seconds.",
            "I generated all the requested boilerplate code for {component}.",
            "Network routes for {component} have been established reliably.",
            "System backup for {component} finalized seamlessly.",
            "Performance profiling of {component} is now complete.",
            "The translation of the {component} strings has been finished.",
            "Excellent news, the rigorous load test on {component} passed."
        ],
        "ui_contexts": ["Task Complete", "Success", "Finished", "Agent Status: Idle", "Completed", "Done"],
        "buttons": ["Follow Up,Show,Dismiss", "New Task,Show", "Done", "View Result", "Start Next,Dismiss", "Follow Up,Hide"],
        "allow_empty_buttons": True
    }
}

# 35 Unique edge cases directly mapped to correct types
EDGE_CASES = [
    ("The process failed. Do you want me to delete the corrupted folder and retry?", "Yes,No", "Terminal Output", "PERMISSION"),
    ("Rate limit hit. I am paused. Please manually solve the captcha to continue.", "View,Unblock", "Action Required", "BLOCKED"),
    ("I recommend upgrading the library, but it might break existing tests. Should I do it?", "Reply", "Prompt", "DECISION"),
    ("Execution finished, but output is entirely empty.", "View Logs,Dismiss", "Agent Status", "ERROR"),
    ("Cannot proceed right now, token quota reached.", "View,Dismiss", "Quota Exceeded", "LIMIT"),
    ("Should I go ahead and execute `rm -rf tmp/`?", "Yes,No", "Terminal Prompt", "PERMISSION"),
    ("TimeoutError: Rate limit of 10req/s exceeded. Process aborted.", "View Logs,Dismiss", "Exception", "LIMIT"),
    ("The command crashed because you need to manually approve the OAuth prompt in your browser.", "Resume", "Blocked", "BLOCKED"),
    ("I finished the code but the linter threw 50 warnings. Do you want me to auto-fix them?", "Yes,No", "Linter Output", "PERMISSION"),
    ("Unable to write to file. The disk quota is exceeded for your account.", "Dismiss", "Warning", "LIMIT"),
    ("I can try to force-push the changes, but it's dangerous. What are your thoughts?", "Reply", "Question", "DECISION"),
    ("The deploy script executed, meaning the server is down. Will attempt restart.", "View Logs", "Info", "ERROR"),
    ("I've completed the analysis. However, the data seems corrupted. Should we re-fetch?", "Yes,No", "Analysis Complete", "DECISION"),
    ("Warning: You are about to exhaust your ChatGPT limits. The script will be paused when that happens.", "Acknowledge", "Quota Alert", "LIMIT"),
    ("Failed to find the file. Should I create a new one instead?", "Yes,No", "Exception Response", "DECISION"),
    ("Execution halted. You must enter your 2FA hardware key to resume the test.", "View,Cancel", "Process Halted", "BLOCKED"),
    ("Database migrated successfully, but 5 rows were inexplicably dropped. I'm stopping here.", "View Details", "Success", "ERROR"),
    ("I notice you are using var instead of const. Do you want me to update the entire file?", "Yes,No", "Suggestion", "PERMISSION"),
    ("This feature is not supported in the free tier of the API. Upgrade required.", "Upgrade,Dismiss", "Error", "LIMIT"),
    ("I've prepared the email campaign. Am I cleared to send it to 10k users?", "Send,Cancel", "Campaign Draft", "PERMISSION"),
    ("Got a 403 Forbidden. I am locked out until you confirm the email link.", "Unblock", "API Error", "BLOCKED"),
    ("The build is green, but performance tanked by 40%. Want me to revert the PR?", "Yes,No", "Build Complete", "DECISION"),
    ("I found a severe security hole. I strongly advise stopping the deployment. Thoughts?", "Reply", "Security Audit", "DECISION"),
    ("I am stuck. The system is asking if we want to overwrite the existing file.", "Reply", "Prompt", "PERMISSION"),
    ("Quota exceeded for Anthropic Claude. The agent has crashed and cannot continue.", "View", "Quota Exceeded", "ERROR"),
    ("I ran the tests, but they were cancelled halfway because the license expired.", "View Details", "Complete", "LIMIT"),
    ("The background job finished. Do you want to run the cleanup script now?", "Execute,Skip", "Job Done", "PERMISSION"),
    ("Execution paused due to potential infinite loop detected. Do you want to proceed anyway?", "Proceed,Abort", "Warning", "PERMISSION"),
    ("Suggestion: This endpoint is terribly slow. Should I rewrite it in Rust?", "Reply", "Optimization Hint", "DECISION"),
    ("Task aborted. I cannot bypass the Cloudflare challenge without human help.", "Fix Manually", "Task Failed", "BLOCKED"),
    ("Your spending limit has been reached, causing the database to go into read-only mode.", "View", "Error", "LIMIT"),
    ("The API call succeeded, but the payload is empty. This is likely an error. Re-run?", "Yes,No", "Success", "DECISION"),
    ("Warning: File exists. Overwrite?", "Yes,No", "File Conflict", "PERMISSION"),
    ("I highly recommend running a security scan. Shall I initiate it now?", "Yes,No", "Recommendation", "PERMISSION"),
    ("App crashed due to an out of memory error caused by reaching the usage limit.", "Dismiss", "Alert", "LIMIT")
]

# Long verbose strings generation
LONG_POOLS = {
    "ERROR": [
        ["The agent encountered a catastrophic failure during execution.", "I was trying to process the component when a sudden error occurred.", "An unexpected exception was thrown from deep within the core architecture.", "Execution abruptly stopped due to a fatal crash in the backend.", "I hit a severe roadblock that caused the entire process to crash."],
        ["The logs indicate a segmentation fault or a null reference somewhere in the pipeline.", "It looks like the system ran out of heap memory and forcefully terminated the worker thread.", "A critical dependency seems to be missing or corrupted on the server side.", "The database connection was inexplicably dropped right in the middle of a transaction.", "A syntax error was encountered while parsing the newly generated script."],
        ["We cannot proceed further until this is investigated and manually resolved by a developer.", "I have saved the stack trace and core dump for your review when you are ready.", "All automated retries failed consistently, so the pipeline is fully halted right now.", "This appears to be an unrecoverable state, meaning the agent is completely dead.", "The stack trace points to a core library that we don't have direct control over."],
        ["Please check the output logs to identify the exact line number of the crash.", "I strongly suggest looking at the related configuration files before trying to restart.", "The process has been safely aborted to prevent any data corruption.", "You might need to debug this locally to understand what went wrong.", "I'd recommend rolling back the latest commit if you can't find a hotfix immediately."]
    ],
    "BLOCKED": [
        ["The execution is currently paused because we hit an interactive prompt.", "I'm currently stuck at a screen that requires human verification to proceed.", "The task has been suspended indefinitely because of a blocking security challenge.", "I cannot move forward automatically because I've encountered a CAPTCHA.", "The agent workflow is currently halted at a strict authentication gateway."],
        ["The system is demanding a manual 2FA code or a hardware key tap.", "A modal dialog box popped up and I cannot programmatically click the confirm button.", "I need someone to manually solve the puzzle presented by the web application.", "The SSH session is asking for a password, but I don't have it stored in my secrets.", "An unexpected terms of service scroll-wall requires a physical user to accept it."],
        ["Please take over the session momentarily to clear this hurdle.", "I will wait here until you manually input the required credentials.", "Once you solve the challenge, the agent will resume its automated tasks.", "You'll need to jump into the active browser window and bypass the security check.", "Click the unblock button after you've handled the external verification."],
        ["If this isn't resolved soon, the session might time out entirely.", "I'll hold my state in memory so we don't lose any progress.", "This is a common issue with highly secure endpoints, so manual intervention is expected.", "Let me know once you've cleared the prompt so I can continue my work.", "I'll standby for instructions."]
    ],
    "PERMISSION": [
        ["I have formulated a plan to execute the requested changes.", "The draft implementation is ready and waiting for your final review.", "I'm about to run a script that will permanently modify the production database.", "I prepared the refactoring changes for the legacy codebase.", "The deployment pipeline configuration has been generated successfully."],
        ["Before I proceed, I need your explicit authorization to run these destructive commands.", "Do I have your permission to overwrite the existing files with the new logic?", "I need you to approve this action because it will drop the current user tables.", "Please confirm that you want me to push these changes directly to the main branch.", "I am requesting elevated privileges to apply these system-wide settings."],
        ["This operation cannot easily be undone once it starts.", "Make sure you have backed up the important data before giving me the green light.", "Review the planned modifications in the diff provided below.", "If you reject this, I can try to come up with a safer, alternative approach.", "If everything looks good to you, simply click allow to begin the process."],
        ["I'll stand by until I receive your explicit confirmation.", "Let me know if you want me to adjust the plan before executing.", "Awaiting your command to initiate the sequence.", "Your approval guarantees that the risk has been assessed and accepted by a human.", "We are clear to launch pending your say-so."]
    ],
    "LIMIT": [
        ["I was making good progress, but we've unfortunately hit a usage cap.", "The API request failed because we exceeded the allocated rate limit.", "Your account has run out of tokens or credits for this specific model.", "The background task was aborted due to hitting a strict daily quota.", "We are approaching the maximum spending limit defined in your workspace settings."],
        ["The server responded with a strictly enforced 429 Too Many Requests error.", "The AI context window is completely full and cannot ingest any more information.", "Our cloud provider is restricting further API calls until the next billing cycle.", "The maximum execution time of 5 minutes was surpassed, halting the worker.", "I'm being throttled by the external service to prevent system degradation."],
        ["We will need to wait for the quota to reset or upgrade the current plan.", "You might want to summarize the previous context to free up some space.", "I will automatically back off and try again when the rate limit window expires.", "Consider managing your subscription tier if this task requires higher volume.", "Please check your billing dashboard to resolve the outstanding resource limits."],
        ["I'll pause execution for now to prevent unnecessary errors.", "Let me know if you manage to increase the quota so I can resume.", "This is a hard platform limit that we cannot easily bypass with code.", "I have saved the intermediate state so we can pick up where we left off later.", "We can try alternative free APIs if you prefer."]
    ],
    "DECISION": [
        ["I've reached a fork in the road regarding the current implementation.", "There are a few different architectural approaches we could take here.", "I'm not entirely sure how you want to handle this specific edge case.", "We have a decision to make about the frontend framework integrations.", "I need your input to resolve an ambiguity in the project requirements."],
        ["Option A is faster to build but might be harder to scale later on.", "We could use a relational database, or we might opt for a NoSQL approach.", "I found multiple matching files, and I don't know which one you want me to edit.", "The library has both a synchronous and an asynchronous API available.", "We can implement infinite scrolling or a traditional pagination component."],
        ["Which path makes the most sense for the long-term vision of this product?", "Please reply with your preference so I can tailor the rest of the code.", "What is the expected behavior when a user logs out during a transaction?", "Let me know your thoughts on the tradeoffs between these two solutions.", "How would you like me to handle errors that occur during the initial load?"],
        ["I'll pause writing the code until I hear back from you.", "Your guidance here will fundamentally shape how the rest of the module is built.", "Take your time to decide, and just reply when you are ready.", "If you prefer, I can also just pick the standard best practice and move on.", "I rely on your domain knowledge for this."]
    ],
    "RECOMMEND": [
        ["During my analysis of the codebase, I noticed a few areas for improvement.", "I was looking through the recently added features and found something interesting.", "The code works perfectly fine, but I wanted to make a quick suggestion.", "I've run some static analysis on the project and formulated a recommendation.", "While building out the requested module, I spotted a minor code smell."],
        ["The algorithm you are currently using has a high time complexity and could be optimized.", "This specific third-party dependency is deprecated and currently poses a security risk.", "You are repeating a lot of CSS rules that could easily be extracted into a shared class.", "The database queries in the loop will likely result in an N+1 performance issue.", "I noticed there are no unit tests covering the core logic of the billing system."],
        ["You don't have to fix this right now, but it's worth keeping in mind for the future.", "Consider utilizing memoization to cache the results and speed up the rendering.", "I would highly advise migrating this component to TypeScript for better type safety.", "Adding a simple try-catch block here could prevent silent failures in production.", "It might make sense to decouple these two services to improve modularity."],
        ["Feel free to ignore this if it's not a priority at the moment.", "If you want, I can automatically apply these suggestions in a separate PR.", "I just wanted to flag this so it doesn't become technical debt down the line.", "Let me know if you'd like me to explain my reasoning in more detail.", "I can implement this right now or we can postpone it."]
    ],
    "COMPLETED": [
        ["I have successfully finished the task you assigned to me.", "The deployment process has concluded without any major issues.", "All requested code changes have been implemented and pushed.", "I've carefully followed your instructions and the feature is now complete.", "The massive refactoring effort has successfully wrapped up."],
        ["I ran the entire test suite, and every single unit test is passing perfectly.", "The newly provisioned infrastructure is live and ready to accept traffic.", "The data migration script processed millions of rows without a single failure.", "I've heavily documented the new architecture in the repository wiki.", "The bug has been fixed, and the application now behaves exactly as expected."],
        ["You can view the final result by checking the local development server.", "Everything looks solid on my end, so I'm moving back to an idle state.", "I'm ready for the next challenge whenever you are.", "Take a look at the attached diff summary to verify the changes yourself.", "I've cleaned up all the temporary files that were generated during the execution."],
        ["Let me know if you need any follow-up tweaks to this implementation.", "We can immediately move on to the next phase of the project if you want.", "I'm standing by, fully prepared to tackle whatever you throw at me next.", "Great job coordinating this! The integration was seamlessly executed.", "I am powering down the active session until you call me again."]
    ]
}

def generate_examples():
    records = []
    
    # 1. Generate standard examples (approx 160 per category)
    for event_type, details in EVENT_TYPES.items():
        templates = details["templates"]
        ui_contexts = details["ui_contexts"]
        button_sets = details["buttons"]
        allow_empty = details.get("allow_empty_buttons", False)
        
        for _ in range(160):
            template = random.choice(templates)
            component = random.choice(COMPONENTS)
            tool = random.choice(TOOLS)
            
            msg = template.format(component=component)
            
            if random.random() < 0.3:
                msg = f"[{tool}] {msg}"
            elif random.random() < 0.15:
                msg = f"({tool}) - {msg}"
                
            if random.random() < 0.1:
                msg = msg.lower()
                
            ui_ctx = random.choice(ui_contexts)
            if random.random() < 0.2:
                ui_ctx = f"{tool} {ui_ctx}"
                
            # 20% random chance of buttons_present = "" if allowed
            if allow_empty and random.random() < 0.2:
                buttons = ""
            else:
                buttons = random.choice(button_sets)
            
            records.append({
                "message_text": msg,
                "buttons_present": buttons,
                "ui_context": ui_ctx,
                "event_type": event_type
            })

    # 2. Add 25 long-form examples per type
    for event_type, details in EVENT_TYPES.items():
        long_pools = LONG_POOLS[event_type]
        ui_contexts = details["ui_contexts"]
        button_sets = details["buttons"]
        allow_empty = details.get("allow_empty_buttons", False)
        
        for _ in range(25):
            # Combine 3 or 4 sentences from the pools
            num_sentences = random.choice([3, 4])
            chosen_sentences = []
            for i in range(num_sentences):
                # Pick a sentence from the i-th pool (wrapping around if necessary)
                pool = long_pools[i % len(long_pools)]
                chosen_sentences.append(random.choice(pool))
                
            msg = " ".join(chosen_sentences)
            tool = random.choice(TOOLS)
            
            if random.random() < 0.2:
                msg = f"[{tool}] {msg}"
            
            ui_ctx = random.choice(ui_contexts)
            
            if allow_empty and random.random() < 0.2:
                buttons = ""
            else:
                buttons = random.choice(button_sets)
                
            records.append({
                "message_text": msg,
                "buttons_present": buttons,
                "ui_context": ui_ctx,
                "event_type": event_type
            })

    # 3. Add ambiguous edge cases
    for msg, btns, ui_ctx, ev_type in EDGE_CASES:
        tool = random.choice(TOOLS)
        if random.random() < 0.3:
            msg = f"[{tool}] {msg}"
            
        records.append({
            "message_text": msg,
            "buttons_present": btns,
            "ui_context": ui_ctx,
            "event_type": ev_type
        })
            
    # Shuffle the dataset
    random.shuffle(records)
    return records


if __name__ == "__main__":
    data = generate_examples()
    
    headers = ["message_text", "buttons_present", "ui_context", "event_type"]
    
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
            
    print(f"Generated {len(data)} training examples across {len(EVENT_TYPES)} types in {OUTPUT_FILE}")
