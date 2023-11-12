# Library Backend Server

### How to run Docker container
1. Navigate to this folder via `cd` command in terminal
2. Build image using `docker build -t library-server`
3. Run container using `docker run -d -p 5000:5000 --name server-container library-server`
4. Use API to upload files and download files
    - Note that the API requires both a .csv Entry/Exit file, as well as section capacities .json file to be uploaded 
    - Can use server-test.ipynb to test out API