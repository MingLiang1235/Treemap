<?php
/***************************************************************************

 * Copyright (c) 2019 Treemap.me, Inc. All Rights Reserved
 * 
**************************************************************************/



/**
 * @file Treemap_api.php 
 * @author unicoder(unicoder@sohu.com)
 * @date 2019/10/23 00:00:00
 * @brief 
 *  
 **/

define("CURL_TIMEOUT",   10); 
define("URL",            "http://127.0.0.1:15000/api/treat_data"); 
define("APP_ID",         "201910011157381"); //替换为您的APPID
define("SEC_KEY",        "kE8I1yruXRsMyfIBsOsu");//替换为您的密钥
define("SITES",          array(
                                array( 'name'=>"Google", 'pos'=>array(0,0), 'w'=>0, 'h'=>0, 'size'=>637313000 ),
                                array( 'name'=>"Runoob", 'pos'=>array(0,0), 'w'=>0, 'h'=>0, 'size'=>13953500170 ),
                                array( 'name'=>"jd",     'pos'=>array(0,0), 'w'=>0, 'h'=>0, 'size'=>56790216020 )
                                array( 'name'=>"suning", 'pos'=>array(0,0), 'w'=>0, 'h'=>0, 'size'=>1592925)));

//获取树图入口
function treemap($width, $height)
{
    $args = array(
        'appid' => APP_ID,
        'salt' => rand(10000,99999),
        'width' => $width,
        'height' => $height,
        'sites' => SITES

    );
    $args['sign'] = buildSign(APP_ID, $args['salt'], SEC_KEY);
    $ret = call(URL, $args);
    $ret = json_decode($ret, true);
    return $ret; 
}

//加密
function buildSign($appID, $salt, $secKey)
{/*{{{*/
    $str = $appID . $salt . $secKey;
    $ret = md5($str);
    return $ret;
}/*}}}*/

//发起网络请求
function call($url, $args=null, $method="post", $testflag = 0, $timeout = CURL_TIMEOUT, $headers=array())
{/*{{{*/
    $ret = false;
    $i = 0; 
    while($ret === false) 
    {
        if($i > 1)
            break;
        if($i > 0) 
        {
            sleep(1);
        }
        $ret = callOnce($url, $args, $method, false, $timeout, $headers);
        $i++;
    }
    return $ret;
}/*}}}*/

function callOnce($url, $args=null, $method="post", $withCookie = false, $timeout = CURL_TIMEOUT, $headers=array())
{/*{{{*/
    $ch = curl_init();
    if($method == "post") 
    {
        $data = convert($args);
        curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
        curl_setopt($ch, CURLOPT_POST, 1);
    }
    else 
    {
        $data = convert($args);
        if($data) 
        {
            if(stripos($url, "?") > 0) 
            {
                $url .= "&$data";
            }
            else 
            {
                $url .= "?$data";
            }
        }
    }
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_TIMEOUT, $timeout);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
    if(!empty($headers)) 
    {
        curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    }
    if($withCookie)
    {
        curl_setopt($ch, CURLOPT_COOKIEJAR, $_COOKIE);
    }
    $r = curl_exec($ch);
    curl_close($ch);
    return $r;
}/*}}}*/

function convert(&$args)
{/*{{{*/
    $data = '';
    if (is_array($args))
    {
        foreach ($args as $key=>$val)
        {
            if (is_array($val))
            {
                foreach ($val as $k=>$v)
                {
                    $data .= $key.'['.$k.']='.rawurlencode($v).'&';
                }
            }
            else
            {
                $data .="$key=".rawurlencode($val)."&";
            }
        }
        return trim($data, "&");
    }
    return $args;
}/*}}}*/

echo treemap(500,100)

?>
