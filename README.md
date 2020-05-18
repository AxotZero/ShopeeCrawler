# ShopeeCrawler
This project is to get product information data from Shoppee Search by chrome driver.

![](https://i.imgur.com/1FW4ASh.png)

The feature you can get is shown below

## arguments
| argument | default | description |
| -------- | -------- | -------- |
| -dp, --driver_path     | ''     | path to your chrome driver     |
| -t, --sleep_time     |  0    |  sleep_time after your driver get info    |
| -k, --keyword     | None     | search keyword     |
| -p, --pages     | [0, 0]     | your start page and end page     |


## column_name
| feature_name | description | 
| -------- | -------- | 
| product_name     | 商品名稱 / 標題     | 
| page     | 商品在搜尋結果的第幾頁     | 
| avg_price     | 商品價錢(因為價錢可能是xxx-xxx所以會取平均)     | 
| rating     | 商品評價     | 
| comments_num     |  評價人數    | 
| sold_num     | 賣出數     | 
| style_num     | 商品有多少種樣式/規格     | 
| img_num     | 商品的圖片數量     | 
| description_len     | 商品描述的字數     | 
| remain_num     | 商品剩餘的數量     | 
| transport_free     | 多少錢免運     | 
| seller_name     | 賣家名字     |
| product_num     | 賣家商品數     | 
| watching     | 賣家關注的人的數量     | 
| response_rating     | 聊聊表現     | 
| canceled_rate     | 取消率     | 
| follower_num     | 追蹤者人數     | 
| comment_rating     | 賣家評價分數     | 
| comment_num     | 賣家評分人數     | 


