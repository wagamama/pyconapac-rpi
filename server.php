<?php

require_once("SQLiter.php");
$db = new SQLiter("../db/pycon2015.db");

$err = array('not_found'    => 'NOT FOUND',
            'no_uid_send'   => 'NO UID SEND',
            'no_such_uid'   => 'NO SUCH UID');

if ( isset($_POST))
{
    switch ($_POST['action'])
    {
        case 'tshirt-query':
            if ( isset($_POST['uid']))
            {
                $r = $db->select(
                        array('reg_no', 'nickname', 'tshirt', 'tshirt_wtime')
                )->from('regist')->where(
                    array(
                        'uid' => $_POST['uid'],
                    )
                )->get();

                if ( ! empty($r) )
                {
                    $result = array(
                        'status' => 'ok',
                        'result' => array('reg_no' => $r[0]['reg_no'],
                                        'nickname' => $r[0]['nickname'],
                                        'tshirt'   => $r[0]['tshirt'],
                                        'tshirt_wtime' => $r[0]['tshirt_wtime']),
                    );
                }
                else
                {
                    $result = array(
                        'status' => 'fail',
                        'result' => array('reg_no' => $err['not_found'],
                                        'nickname' => $err['not_found'],
                                        'tshirt'   => $err['not_found'],
                                        'tshirt_wtime' => $err['not_found'])
                    );
                }

                echo json_encode($result);
            }
            else
            {
                $result = array(
                    'status' => 'fail',
                    'result' => array('reg_no' => $err['no_uid_send'],
                                    'nickname' => $err['nickname'],
                                    'tshirt'   => $err['no_uid_send'],
                                    'tshirt_wtime' => $err['no_uid_send'])
                );

                echo json_encode($result);
            }

        break;

        case 'tshirt-update':
            if ( isset($_POST['uid']))
            {

                $r = $db->select(
                        array('reg_no', 'nickname', 'tshirt', 'tshirt_wtime')
                )->from('regist')->where(
                    array(
                        'uid' => $_POST['uid'],
                    )
                )->get();

                if ( ! empty($r) )
                {
                    $db->update(
                        array('tshirt_wtime' => $_POST['tshirt_wtime'])
                    )->set('regist')->where(
                        array('uid' => $_POST['uid'])
                    )->execute();

                    $result = array('status' => 'ok',
                                    'result' => array('uid' => $_POST['uid'],
                                                    'tshirt_wtime' => $_POST['tshirt_wtime'])
                                );
                }
                else
                {
                    $result = array('status' => 'fail',
                                    'result' => array('reg_no' => $err['no_such_uid'],
                                                    'tshirt' => $err['no_such_uid'],
                                                    'tshirt_wtime' => $err['no_such_uid'])
                                );

                }

                echo json_encode($result);
            }
            else
            {
                $result = array(
                    'status' => 'fail',
                    'result' => array('reg_no' => $err['no_uid_send'], 'tshirt' => $err['no_uid_send'], 'tshirt_wtime' => $err['no_uid_send'])
                );

                echo json_encode($result);
            }
        break;



        case 'regist-update':
            if ( isset($_POST['reg_no']) && isset($_POST['uid']) )
            {
                $r = $db->select('*')->from('regist')->where(array('reg_no' => $_POST['reg_no']))->get();

                if ( count($r) == 0)
                {
                    $result = array('status' => 'fail',
                                    'result' => array('reg_no' => $_POST['reg_no'],
                                                    'uid' => 'NOT FOUND!',
                                                    'nickname' => 'NOT FOUND!')
                                    );
                }
                else
                {
                    $db->update(
                        array('uid' => $_POST['uid'],
                            'regist_wtime' => $_POST['regist_wtime'])
                    )->set('regist')->where(
                        array('reg_no' => $_POST['reg_no'])
                    )->execute();

                    $result = array('status' => 'ok',
                                    'result' => array('reg_no' => $r[0]['reg_no'],
                                                    'uid' => $r[0]['uid'],
                                                    'nickname' => $r[0]['nickname'])
                                );
                }

                echo json_encode($result);
            }
        break;


        case 'query':
            if ( isset($_POST['uid']))
            {
                $r = $db->select('*')->from('regist')->where(array('uid' => $_POST['uid']))->get();

                if ( count($r) == 0)
                {
                    $result = array('status' => 'fail',
                                    'result' => array('reg_no' => 'NOT FOUND!',
                                                    'uid' => $_POST['uid'],
                                                    'nickname' => 'NOT FOUND!',
                                                    'regist_wtime' => 'NOT FOUND',
                                                    'tshirt_wtime' => 'NOT FOUND')
                                    );
                }
                elseif ( count($r) == 1)
                {
                    $result = array('status' => 'ok',
                                    'result' => array('reg_no' => $r[0]['reg_no'],
                                                    'uid' => $r[0]['uid'],
                                                    'nickname' => $r[0]['nickname'],
                                                    'regist_wtime' => $r[0]['regist_wtime'],
                                                    'tshirt_wtime' => $r[0]['tshirt_wtime'])
                                    );
                }
                else
                {
                    $str = '';
                    foreach ($r as $v)
                    {
                        $str = $str . $v['reg_no'] . ", ";
                    }

                    $result = array('status' => 'fail',
                                    'result' => array('reg_no' => 'OVER ONE RECORD!',
                                                    'uid' => $_POST['uid'],
                                                    'nickname' => $str,
                                                    'regist_wtime' => 'OVER ONE RECORD!',
                                                    'tshirt_wtime' => 'OVER ONE RECORD!')
                                    );
                }

                echo json_encode($result);

            }
        break;



    }
}

