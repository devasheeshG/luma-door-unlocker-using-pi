# Auth Flow

### Request

POST /auth/sign-in-with-password HTTP/2
Host: api.lu.ma
Cookie: luma.did=deyiot7y83llvf6xbuij73wmq49aq7; luma.first-page=%2F; __cf_bm=yJYbh8LF09NWXyKv.D98vyQTmZ2hvYQVXNowPou_kB8-1752408814-1.0.1.1-n5Arl3FciF5E.KYGb_5zaEWkLFKIaShVNXX4TXGS0Xswh0W6QdZL3A6wIokn4NocUGLjxLUdm52DFSDteMFOSzsJLkuXbsSqA1ZE3PrkfFY; luma.native-referrer=https%3A%2F%2Flu.ma%2F
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en
Accept-Encoding: gzip, deflate, br
Referer: https://lu.ma/
X-Luma-Client-Version: d799f2bcdceec685f55811350f8eeffc67534a5f
X-Luma-Web-Url: https://lu.ma/signin
X-Luma-Client-Type: luma-web
Content-Type: application/json
Content-Length: 50
Origin: https://lu.ma
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
Priority: u=0
Te: trailers

{"email":"sfo@zo.xyz","password":"GHI6ED62Qw000N"}

### Response

HTTP/2 200 OK
Date: Sun, 13 Jul 2025 12:28:55 GMT
Content-Type: application/json; charset=utf-8
Set-Cookie: luma.auth-session-key=usr-oUTIxE0c8yIomEz.8w2rcdyoxx5w8obal1v4; path=/; expires=Thu, 11 Sep 2025 12:28:55 GMT; domain=.lu.ma; samesite=lax; secure; httponly
Set-Cookie: __cf_bm=yswqrDC0qaauWpTdrYYvEjHwiocE3rVnOoE9ltqxdg0-1752409735-1.0.1.1-UVIQhUZ8plb8enf80zANQY2CYkKLiXHO3HW8igFk6ZGVqcNE5BIghsEN0.IRqnvgboyMsPgIskPdWg2DU9nObVvLzZQceV.OZw3X80PEIxQ; path=/; expires=Sun, 13-Jul-25 12:58:55 GMT; domain=.lu.ma; HttpOnly; Secure; SameSite=None
Vary: Origin
Access-Control-Allow-Origin: https://lu.ma
Access-Control-Allow-Credentials: true
Cf-Cache-Status: DYNAMIC
Strict-Transport-Security: max-age=2592000; preload
X-Robots-Tag: noindex
Server: cloudflare
Cf-Ray: 95e8c86c5949ebe2-SJC

{"centrifugo_user_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c3Itb1VUSXhFMGM4eUlvbUV6IiwiZXhwIjoxNzU1MDg4MTM1LCJpYXQiOjE3NTI0MDk3MzV9.Ufq6x50bdOcEDvgi6lEumbvAdBJwnxoXJVzhoisStMY","is_blocked":false,"deleted_at":null,"api_id":"usr-oUTIxE0c8yIomEz","apple_email":null,"apple_user_id":null,"avatar_url":"https://images.lumacdn.com/avatars/et/4ce4fb84-b66e-47d8-bbf2-7f5a31d8c5a9","bio_short":"I'm the coolest techno-optimist clubhouse in San Francisco","company":null,"created_at":"2024-05-20T05:02:35.274Z","email_verified":true,"email":"sfo@zo.xyz","eth_address":null,"eth_ens_name":null,"first_name":"Zo San","geo_city":"San Francisco","geo_country":"US","geo_region":"California","google_contacts_sync_enabled":false,"google_email":"sfo@zo.xyz","google_user_id":"117266604434197160859","google_scopes":["https://www.googleapis.com/auth/contacts.readonly","https://www.googleapis.com/auth/userinfo.email","https://www.googleapis.com/auth/userinfo.profile","openid"],"has_luma_chat_app":true,"has_password":true,"instagram_handle":"zohouseofficial","is_admin":false,"last_name":"Francisco","last_online_at":"2025-07-13T12:16:46.153Z","last_signed_in_at":"2025-07-13T12:16:04.760Z","linkedin_handle":null,"locale":"en","name":"Zo House SF","notification_preferences":{"version":"2024-10-21","event_guest__blast":{"sms":false,"push":false,"email":false},"event_guest__invite":{"sms":true,"push":true,"email":true},"event_guest__update":{"push":true,"email":true},"event_guest__reminder":{"sms":false,"push":false,"email":false},"luma__product_updates":{"email":false},"event_host__guest_registered":{"push":false,"email":false},"event_guest__feedback_request":{"email":false},"event_host__feedback_received":{"email":false},"calendar_admin__new_member_joined":{},"calendar_admin__new_event_submitted":{"email":false}},"personal_calendar_api_id":"cal-d9daDIfEHC220z2","phone_number":null,"preferred_theme":"system","solana_address":null,"stripe_customer_id":null,"support_roles":null,"tiktok_handle":null,"timezone":"America/Los_Angeles","twitter_handle":"SFOxZo","two_factor_auth_enforced":false,"updated_at":"2025-07-13T12:16:58.184Z","username":"SFOxZo","website":null,"youtube_handle":"sfoxzo","zoom_user_email":null,"zoom_user_id":null,"zoom_webinar_enabled":false,"google_meet_enabled":false,"user":{"centrifugo_user_token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c3Itb1VUSXhFMGM4eUlvbUV6IiwiZXhwIjoxNzU1MDg4MTM1LCJpYXQiOjE3NTI0MDk3MzV9.Ufq6x50bdOcEDvgi6lEumbvAdBJwnxoXJVzhoisStMY","is_blocked":false,"deleted_at":null,"api_id":"usr-oUTIxE0c8yIomEz","apple_email":null,"apple_user_id":null,"avatar_url":"https://images.lumacdn.com/avatars/et/4ce4fb84-b66e-47d8-bbf2-7f5a31d8c5a9","bio_short":"I'm the coolest techno-optimist clubhouse in San Francisco","company":null,"created_at":"2024-05-20T05:02:35.274Z","email_verified":true,"email":"sfo@zo.xyz","eth_address":null,"eth_ens_name":null,"first_name":"Zo San","geo_city":"San Francisco","geo_country":"US","geo_region":"California","google_contacts_sync_enabled":false,"google_email":"sfo@zo.xyz","google_user_id":"117266604434197160859","google_scopes":["https://www.googleapis.com/auth/contacts.readonly","https://www.googleapis.com/auth/userinfo.email","https://www.googleapis.com/auth/userinfo.profile","openid"],"has_luma_chat_app":true,"has_password":true,"instagram_handle":"zohouseofficial","is_admin":false,"last_name":"Francisco","last_online_at":"2025-07-13T12:16:46.153Z","last_signed_in_at":"2025-07-13T12:16:04.760Z","linkedin_handle":null,"locale":"en","name":"Zo House SF","notification_preferences":{"version":"2024-10-21","event_guest__blast":{"sms":false,"push":false,"email":false},"event_guest__invite":{"sms":true,"push":true,"email":true},"event_guest__update":{"push":true,"email":true},"event_guest__reminder":{"sms":false,"push":false,"email":false},"luma__product_updates":{"email":false},"event_host__guest_registered":{"push":false,"email":false},"event_guest__feedback_request":{"email":false},"event_host__feedback_received":{"email":false},"calendar_admin__new_member_joined":{},"calendar_admin__new_event_submitted":{"email":false}},"personal_calendar_api_id":"cal-d9daDIfEHC220z2","phone_number":null,"preferred_theme":"system","solana_address":null,"stripe_customer_id":null,"support_roles":null,"tiktok_handle":null,"timezone":"America/Los_Angeles","twitter_handle":"SFOxZo","two_factor_auth_enforced":false,"updated_at":"2025-07-13T12:16:58.184Z","username":"SFOxZo","website":null,"youtube_handle":"sfoxzo","zoom_user_email":null,"zoom_user_id":null,"zoom_webinar_enabled":false,"google_meet_enabled":false},"signed_in":true,"auth_token":"usr-oUTIxE0c8yIomEz.8w2rcdyoxx5w8obal1v4"}


# QR Code Data

https://lu.ma/check-in/evt-6SAYBD09zCBjNNg?pk=g-r3DlcAelLjxttUG

# Checkin flow (+ve)

## Request

GET /event/admin/get-guest?event_api_id=evt-6SAYBD09zCBjNNg&proxy_key=g-r3DlcAelLjxttUG HTTP/2
Host: api.lu.ma
Cookie: luma.did=deyiot7y83llvf6xbuij73wmq49aq7; luma.first-page=%2F; __cf_bm=yswqrDC0qaauWpTdrYYvEjHwiocE3rVnOoE9ltqxdg0-1752409735-1.0.1.1-UVIQhUZ8plb8enf80zANQY2CYkKLiXHO3HW8igFk6ZGVqcNE5BIghsEN0.IRqnvgboyMsPgIskPdWg2DU9nObVvLzZQceV.OZw3X80PEIxQ; luma.native-referrer=https%3A%2F%2Flu.ma%2F; luma.auth-session-key=usr-oUTIxE0c8yIomEz.8w2rcdyoxx5w8obal1v4
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en
Accept-Encoding: gzip, deflate, br
Referer: https://lu.ma/
X-Luma-Client-Version: 0b8c207761d88a135efa0dcd3fdf8ab037463497
X-Luma-Web-Url: https://lu.ma/check-in/evt-6SAYBD09zCBjNNg/scan
X-Luma-Client-Type: luma-web
Origin: https://lu.ma
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
Priority: u=4
Te: trailers

## Response

HTTP/2 200 OK
Date: Sun, 13 Jul 2025 12:43:53 GMT
Content-Type: application/json; charset=utf-8
Vary: Origin
Access-Control-Allow-Origin: https://lu.ma
Access-Control-Allow-Credentials: true
Cf-Cache-Status: DYNAMIC
Strict-Transport-Security: max-age=2592000; preload
X-Robots-Tag: noindex
Server: cloudflare
Cf-Ray: 95e8de590f7815ca-SJC

{"guest":{"api_id":"gst-YlkJrZpABZVyAZA","approval_status":"approved","created_at":"2025-07-13T09:59:37.848Z","crypto_contract_address":null,"crypto_owner_address":null,"crypto_token_id":null,"crypto_token_info":null,"custom_source":null,"eth_address":null,"event_api_id":"evt-6SAYBD09zCBjNNg","geo_city":"San Francisco","geo_country":"US","invited_at":null,"joined_at":null,"phone_number":null,"proxy_key":"g-r3DlcAelLjxttUG","referred_by_user_api_id":null,"registered_at":"2025-07-13T09:59:37.847Z","registration_answers":[],"solana_address":null,"updated_at":"2025-07-13T10:00:06.172Z","user_api_id":"usr-41Fyq8vbxHSGklo","name":"Anuj Kodam","first_name":"Anuj","last_name":"Kodam","email":"anuj@zo.xyz","avatar_url":"https://images.lumacdn.com/avatars/ek/440a639d-85f5-4812-b623-c1621a0a1fe6","bio_short":"From the world where we have realised our unity and identity with all. \n\nBuilding Products at Zo World. \n\nZooohmm! ","instagram_handle":null,"linkedin_handle":"/in/anuj-k-07ba83102","locale":"en-IN","tiktok_handle":null,"twitter_handle":"aatmaann","website":null,"youtube_handle":"","registered_or_created_at":"2025-07-13T09:59:37.847Z","object":"event_guest","has_joined_event":false,"last_checked_in_at":"2025-07-13T10:00:06.140Z","survey_response_rating":null,"survey_response_feedback":null,"event_tickets":[{"amount":0,"api_id":"eventticket-NtUk0UBq84o7398","currency":"usd","amount_tax":0,"is_captured":false,"charge_api_id":null,"checked_in_at":"2025-07-13T10:00:06.140Z","invalidated_at":null,"amount_discount":0,"event_ticket_type_info":{"name":"Standard","type":"free","cents":null,"api_id":"evtticktyp-q2uth3fLS5F6ig3","currency":null,"is_hidden":false,"min_cents":null,"description":null,"is_flexible":false,"event_api_id":"evt-6SAYBD09zCBjNNg","max_capacity":null,"valid_end_at":null,"currency_info":null,"valid_start_at":null,"require_approval":false,"membership_restriction":null,"ethereum_token_requirements":[]},"event_ticket_type_api_id":"evtticktyp-q2uth3fLS5F6ig3","event_ticket_order_api_id":"evttktord-z5VbP3h9hrhiA0x"}]}}

# Checkin flow (-ve)

## Request

GET /event/admin/get-guest?event_api_id=evt-6SAYBD09zCBjNNg&proxy_key=g-eqzjvbIp6EVYppx HTTP/2
Host: api.lu.ma
Cookie: luma.did=deyiot7y83llvf6xbuij73wmq49aq7; luma.first-page=%2F; __cf_bm=DfTksZNGG5Al_yZqjrWVM5uKiegrhHTwOc1cti2p.yU-1752410728-1.0.1.1-.6n6qscDZ8IkKdJlyDTp3TdpsO6xwT9WsxM9Q0n9z0b8J8kSk2amMD81UctQGdWxjgkryZqWQG1fXbaYa1EcN8VBE9LmYGZqtdm1gPNitmE; luma.native-referrer=https%3A%2F%2Flu.ma%2F; luma.auth-session-key=usr-oUTIxE0c8yIomEz.8w2rcdyoxx5w8obal1v4
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:140.0) Gecko/20100101 Firefox/140.0
Accept: */*
Accept-Language: en
Accept-Encoding: gzip, deflate, br
Referer: https://lu.ma/
X-Luma-Client-Version: 0b8c207761d88a135efa0dcd3fdf8ab037463497
X-Luma-Web-Url: https://lu.ma/check-in/evt-6SAYBD09zCBjNNg/scan
X-Luma-Client-Type: luma-web
Origin: https://lu.ma
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-site
Priority: u=4
Te: trailers

## Response

HTTP/2 404 Not Found
Date: Sun, 13 Jul 2025 12:45:48 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 42
Cf-Ray: 95e8e12bfa637ada-SJC
Vary: Origin
Access-Control-Allow-Origin: https://lu.ma
Access-Control-Allow-Credentials: true
Cf-Cache-Status: DYNAMIC
Strict-Transport-Security: max-age=2592000; preload
X-Robots-Tag: noindex
Server: cloudflare

{"message":"Guest not found.","code":null}
