netchecker
==========

Collect store and analyze your internet provider's usage stats.

- Why?

  - Every ISP provides usage reports - but none that I know of expose any API to consume them.

  - I get alerts when my internet usage reaches 80% of my specified limit. But a user should be able to customize alerts based on thresholds, usage days, 
    etc. Some scenarios in which a user might want to receive alerts:

    - Send alert every 10 days.

    - Send alert when threshold crosses 25%, 50%, 75%, 90% of usage

    - If I am underutilizing my data limit e.g. 5 days left in the billing cycle, consumed only 50% of data plan

  - The alert sources should be configurable - i.e. send mail, send facebook message, etc.

  - Each day's information should be updated in a central store e.g. an excel sheet in google docs, dropbox, etc.

  - User should be able consume the usage information in his/her own way e.g. plot graphs, compare his usage with friends, etc.

  - Tomorrow when you transition to an new ISP (supported by netchecker) - manual effort should be as less as possible (ideally zero) to restart data 
    collection.

- Project Goals:

  - At the outset, this project might seem to be a one stop solution for getting usage info of various internet providers. Doing this is neither scalable
    nor recommended because:
    
    - There are too many internet providers across the world, each with its own quirks in terms of extracting usage information. 

    - We are logging in to each provider's portal, scraping data and displaying it to the user. There is no guarantee that an internet provider will
      keep the process same - a change to the login process or how the data is displayed will break the code.

  - The focus is to add as many providers as there are ways to extract usage data, so that even if the end user's provider is not listed in this repo,
    they can look at a near similar provider's code and add their own. This also means each provider's code should follow a generic, easy to understand
    API to get usage info. As of now, I have identified following ways of extracting information:

    1. Log in to the provider's portal using username/password - the portal being available only when you are on the 
       provider's network (i.e. using internet through their modems), navigate to a specific page and extract information.

    2. No need to login to provider's portal - as long as you are on the provider's network, go to a specific page and
       extract the usage information.

    3. Log in to the provider's portal using username/password - the portal being available on the internet, navigate 
       to a specific page and extract information. 

    4. Log in to the provider's portal using OAuth via gmail/facebook - the portal being available on the internet, 
       navigate to a specific page and extract information.

  - In essence, there are 3 types of providers: nologin, login-passwd, login-oauth. 


- Current status:

  - This project is a work in progress. It started on 29th June, 2014. As of now the feature set is:

    - Check current usage for Airtel.
    - Check current usage and plan details for Railwire

- Usage:

  ``` python
  In [1]: import netchecker.check_provider as check_provider

  In [3]: print check_provider.get_usage('airtel')
  +------------+-----------------+----------------+---------------------+-----------+
  |    Date    | Data Limit (GB) | Data Used (GB) | Data remaining (GB) | Days Left |
  +------------+-----------------+----------------+---------------------+-----------+
  | 2014-06-30 |       60.0      |     25.69      |        34.31        |     4     |
  +------------+-----------------+----------------+---------------------+-----------+

  In [4]: print check_provider.get_usage('railwire')
  +------------+-----------------+---------------------+-------------------+--------------------+
  |    Date    | Data Limit (GB) | Total Download (GB) | Total Upload (GB) |     Total Time     |
  +------------+-----------------+---------------------+-------------------+--------------------+
  | 2014-06-30 |       40.0      |        25.72        |        2.34       | 17 days + 20:22:30 |
  +------------+-----------------+---------------------+-------------------+--------------------+

  In [5]: print check_provider.get_usage('railwire').plan
  +-----------+-------------+-----------------+--------------+
  | Plan name | Time (Days) | Data Limit (GB) | Speed (Mbps) |
  +-----------+-------------+-----------------+--------------+
  | FUP10Mbps |      30     |       40.0      |     10.0     |
  +-----------+-------------+-----------------+--------------+
  ```

- Immediate TODO:

  - Rather than adding providers - add types of providers (nologin, login-passwd, login-oauth, etc.) - and add few examples of each provider.
  - Make check_provider.py a daemon for running periodically.
  - Add notifier - which will send alerts depending on defined thresholds.
  - Add ISP: ACT.
