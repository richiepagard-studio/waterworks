#!/bin/bash


RUNSERVER() {
	echo $(python3 manage.py runserver)
}
MAKEMIGRATIONS() {
	echo $(python3 manage.py makemigrations)
}
MIGRATE() {
	echo $(python3 manage.py migrate)
}
LOCAL_TEST() {
	echo $(python3 manage.py test)
}

##
# Define colors and their functions
##
green='\e[32m'
blue='\e[34m'
clean='\e[0m'

function ColorGreen() {
	echo -ne ${green}$1${clean}
}
function ColorBlue() {
	echo -ne ${blue}$1${clean}
}

##
# Main menu to choose an option
# basic options for a Django project
##
function main_menu() {
	echo -ne "
	What do want to do now?
	$(ColorGreen '1)') Makemigration
	$(ColorGreen '2)') Migrate
	$(ColorGreen '3)') Local Test
	$(ColorGreen '4)') Running Localhost Server
	$(ColorGreen '0)') Exit
	$(ColorBlue 'Choose an option: ')"

	read user_input
	case ${user_input} in
		1) MAKEMIGRATIONS ; main_menu ;;
		2) MIGRATE ; main_menu ;;
		3) LOCAL_TEST ; main_menu ;;
		4) echo $(python3 manage.py runserver) ; main_menu ;;
		0) exit 0 ;;
	esac
}

main_menu
