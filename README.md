netchecker
==========

Single point for checking internet usage, sending alerts and collating data for various internet providers. 

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

  - Tomorrow when you transition to an new ISP (supported by netchecker) - manual effort should be as less as possible to restart data collection

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

  - Add ISP: ACT
  - Provide a way to update daily usage information centrally
  - Make check_provider.py a daemon for running periodically

