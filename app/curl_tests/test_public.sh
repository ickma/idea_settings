#!/usr/bin/env bash
url=127.0.0.1
port=8000
path=/public/1
type=text

#解析帮助命令
while getopts "hm:t:o" opt;do
    case ${opt} in
#    列出命令帮助
        h)
        echo [-h] -m [run/debug] -t [text/image/voice/video/shortvideo] sig/msg
        ;;
       esac

      case ${opt} in
#      获取当前测试模式，对应不同接口 run:8000/debug:8001
      m)
        case ${OPTARG} in
     run)
        ;;
     debug)
        port=8001
        ;;
       esac
      esac
#      获取当前msg测试类型，text/image/voice/video等....
      case ${opt} in
#      是否保存
      o)
      export testing_output=true
      ;;
      t)
        case ${OPTARG} in
        image)
        type=image
            ;;
         video)
         type=video
         ;;
         voice)
         type=voice
         ;;
         event)
         type=event
         ;;
        esac
      esac

done



#清除已解析的参数
shift $((OPTIND-1))

case "$1" in
#响应来自服务器的验证请求
sig)
           python ./create_curl_params.py
;;
#响应来自微信服务器的用户消息
msg)
#        设置当前的测试url环境变量
        export testing_url=${url}:${port}${path}?
#         测试当前测测试类型环境变量
        export testing_type=${type}
        python ./create_xml_request.py
;;
esac


