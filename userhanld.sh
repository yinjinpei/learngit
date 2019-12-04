#!/bin/bash
#批量添加用户



showContent(){
	local content=$1
	local colorFlag=$2
	if [ 'black' == $colorFlag ]; then
		color=30
	elif [ 'red' == $colorFlag ]; then
		color=31
	elif [ 'green' == $colorFlag ]; then
		color=32
	elif [ 'yellow' == $colorFlag ]; then
		color=33
	elif [ 'blue' == $colorFlag ]; then
		color=34
	elif [ 'purple' == $colorFlag ]; then
		color=35
	elif [ 'cyanblue' == $colorFlag ]; then
		color=36
	elif [ 'white' == $colorFlag ]; then
		color=37
	else
		color='36'
	fi
	
	echo -e "\033[${color}m${content}\033[0m" 
}

showHead(){
	showContent '******************************************' 'cyanblue'
	showContent '请选择功能：' 'yellow'
	showContent '	【1】添加用户' 'yellow'
	showContent '	【2】修改密码' 'yellow'
	showContent '	【3】删除用户' 'yellow'
        showContent ' ' 'red'
        showContent '   温馨提示: 用户名输入"exit" 退出程序！  ' 'purple'
        showContent '------------------------------------------' 'purple'
	showContent '******************************************' 'cyanblue'
}

checkUser(){
	id $userName &>/dev/null
	if [ '0' == $? ]; then
		showContent '用户已存在！' 'red'
		return 1
	fi

	if echo "$userName" | grep -q '^[a-zA-Z0-9]\+$'; then
	        showContent '输入用户名正确！' 'green' &>/dev/null
	else
		showContent '输入用户名错误！用户名只仅限于字母和数字组合，请正确输入！' 'red' 
		return 2
	fi

}

addToUser(){
	/usr/sbin/useradd $userName &>/dev/null
	id $userName &>/dev/null
        if [ '0' == $? ]; then
		showContent "`id $userName`" 'green'
		showContent "$userName 添加用户成功" 'green'
	else
		showContent "$userName 添加用户失败！" 'red'
        fi
}

modifyPasswd(){
	read -e -p "请设置${userName}用户的密码: " userPasswd
	echo "$userPasswd" | /usr/bin/passwd $userName --stdin &>/dev/null	
	if [ '0' == $? ]; then
		showContent "$userName 更新密码成功！" 'green'
	else
		showContent "$userName 更新密码失败！" 'red'
	fi
}

deleteUser(){
	/usr/sbin/userdel -r $userName &>/dev/null
	id $userName &>/dev/null
        if [ '0' != $? ]; then
                showContent "$userName 删除用户成功" 'green'
        else
                showContent "$userName 删除用户失败！" 'red'
        fi

}


inputNewUserName(){
	while true
        do
		read -n 30 -e -p "${content} ： "  userName
		exitProgram $userName
		checkUser $userName
		if [ "1" == $? -o "2" == $? ];then
			continue	
		else
			break
		fi
        done
}

exitProgram(){
	if [ 'exit' == $1 ];then
		showContent "退出程序!" 'cyanblue'
		exit
	fi
}

main(){
	userName=
	userPasswd=
	showHead

	while true
	do
		if [[ $funcNO =~ ^[1-3]$ ]];then
			break
		else
			read -n 1 -e -p "请正确输入对应环境的编号  [ 1 - 3 ] ： "  funcNO
			continue
		fi
	done
	
	while true	
	do
		# 1,添加用户
		if [ 1 == $funcNO ];then
			content="请输入新的用户名"
			inputNewUserName $content
			addToUser $userName
			modifyPasswd $userName $userPasswd
		# 2,修改用户密码
		elif [ 2 == $funcNO ];then
			read -e -p "请输入需要更改密码的用户名: " userName
			exitProgram $userName
			modifyPasswd $userName $userPasswd
		# 3,删除用户
		elif [ 3 == $funcNO ];then
			read -e -p "请输入需要删除的用户名: " userName
			exitProgram $userName
			id $userName &>/dev/null
			if [ '0' == $? ]; then
				read -e -p "确定删除${userName}用户? 请输入 y or Y  ,任意键将取消: " verifyCode
				if [ "y" == $verifyCode -o "y" == $verifyCode ];then
					deleteUser $userName
				fi
			else
				showContent "${userName}用户不存在！" 'red'
				exit
			fi
		else
			echo $funcNO
		fi
	done
}


main
