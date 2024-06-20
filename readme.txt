I chose asyncio because of its scalability when compared to using threads in this case.

I didn't have enough time to handle the major issue of github rate limiting access to their APIs.
1. Invoker instance will have a should_sleep attribute that will be init with 0,

2. When that value is not zero all query tasks will sleep for that value before invoking the query.

2. When we get an error response because of the rate limit we will extract the cool off value it
   will contain and update should_sleep attribute.
   (Multiple queries will fail on this because of race condition).

3. All queries that failed because of rate limit will rerun themselves.

4. When a query task is done waiting it will reset should_sleep to 0.

3. Github allows a higher rate limit if you sign up and generate an access token, so that is what must
   be done for production environment. Adding the token will require making some changes to the HttpClient
   class that is in charge of what headers are used in the session with github.


Pip Requirements (python 3.8.2):
aiofiles==23.2.1
aiohttp==3.9.0
pydantic==2.5.3

