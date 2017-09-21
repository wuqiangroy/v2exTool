# v2exTool
It's a tool to help you using v2ex better, you can check in, get the content of each node and more.   
The v2ex website is: `www.v2ex.com`
## How To Use It
`pip install v2extool`    
if you are in china, blocked by GFW     
you can try:     
`pip install v2extool -i https://pypi.douban.com/simple`
### login
`import v2extool`    
`v2extool.login(username="", password="")`    
it will return a success or failed message   
`{"success": "login success"}`    
`{"error": "login failed, please check your username or password"}`   
### check in
`v2extool.check_in`
### get the node's content 
`v2extool.node_content(node_name="")`    
default node_name is tech.    
the node_name you can type chinese or english.    
like this:    
`v2extool.node_content(node_name="creative")`    
`v2extool.node_content(node_name="创意")`
### get personal info
`v2extool.self_info`
### get user info
`v2extool.user_info(username="")`   
or    
`v2extool.user_info(user_id="")`   
and you can type username and id both:    
`v2extool.user_info(username="", user_id="")`   
if you type both but not compare, system will only recognise id.
### get balance
you can get your own balance when login   
`v2extool.balance`   
it will return a list of dict   
like this   
`[{'total_balance': '5013.0'}, {'time': '2017-09-21 09:21:37', 'info': '20170921 的每日登录奖励 33 铜币'}]`
