# -*- coding: utf-8 -*-
"""
Created on Mon May 24 11:13:27 2021

@author: aman
"""
import mysql.connector

#establishing connection and creating database 
mydb = mysql.connector.connect(host="localhost",user="root",passwd="2003")
mycursor = mydb.cursor()
mycursor.execute("create database if not exists passwordvault")
mycursor.execute("use passwordvault")

mycursor.execute("create table if not exists users(name varchar(25), masterpwd varchar(25))")
mycursor.execute("select * from users")
usersread = mycursor.fetchall()
users = dict()
for each in usersread:
    key = each[0]
    value = each[1]
    users[key] = value


def createuser():
    name = input("\nEnter your name : ")
    name = name.lower()
    if name in users.keys():
        print("Oops, name already taken!")
    else : 
        passwd = input("Enter master password for this user : ")
        mycursor.execute("create table "+name+"(Site varchar(25), Userid varchar(35), Passwd varchar(25))")
        mydb.commit()
        command = "insert into users values('{username}', '{userpasswd}')".format(username = name, userpasswd = passwd)
        mycursor.execute(command)
        mydb.commit()
        print("User has been added!")
        
        
def verifymp(name):
    if name in users.keys():
        ip = input("\nEnter master password for user "+name+" : ")
        if ip == users[name] :
            print("Password is correct.")
            return True
        else : 
            print("Incorrect password!")
            return False
    else: 
        print("User", name, "does not exist.")
        return False
    
    
def sitesearch(username):
    sname = input("\nEnter name of website : ")
    command = "select * from "+username+" where Site = '"+sname+"'"
    mycursor.execute(command)
    result = mycursor.fetchall()
    if len(result) != 0 : 
        for each in result :
            print("\nSite name : ", each[0])
            print("Site userid : ", each[1])
            print("Site password : ", each[2])
    else : 
        print("No data found.")
    
    
def accessexisting():
    username = input("\nEnter username without any spaces : ")
    username = username.lower()
    result = verifymp(username)
    if result == True :
        pass
    else : 
        return
    i = "yes"
    while i == "yes" :
        print("\nHere are your options : ")
        print("1. Get login details for a particular site.")
        print("2. Add details of a new site.")
        print("3. Delete some site")
        print("4. Edit some site")
        i = input("\nEnter the number corresponding to your choice : ")
        try : 
            num = int(i)
            if num == 1 : 
                sitesearch(username)
            elif num == 2 : 
                addsite(username)
            elif num == 3 : 
                deletesite(username)
            elif num == 4 : 
                editsite(username)
            else : 
                print("\nInvalid choice, please enter any number from 1 to 4 only.")
        except : 
            print("Please enter numbers from 1 to 4 only.")
        str1 = input("\nEnter 'yes' to continue with this user, or any other character to exit : ")
        i = str1


def deleteuser():
    name = input("\nEnter your name : ")
    name = name.lower()
    if name in users.keys():
        res = verifymp(name)
        if res == True : 
            command = "drop table "+name
            mycursor.execute(command)
            mydb.commit()
            command2 = "delete from users where name = '"+name+"'"
            mycursor.execute(command2)
            mydb.commit()
            del users[name]
            print("user", name, "has been deleted.")
    else : 
        print("User does not exist.")
        
        
def edituser(name):
    if name in users.keys():
        check = verifymp(name)
        if check == True : 
            v1 = input("\nEnter new master password : ")
            v2 = input("Confirm new master password : ")
            if v1 != v2 : 
                print("Passwords do not match. Please try again.")
            else : 
                command = "update users set masterpwd='"+v1+"' where name='"+name+"'"
                mycursor.execute(command)
                mydb.commit()
                users[name] = v1
                print("Password changed successfully.")
    else : 
        print("Sorry, user not found!")
                
                
def addsite(name):
    sname = input("\nEnter name of website : ")
    command = "select Site from "+name
    mycursor.execute(command)
    result = mycursor.fetchall()
    if (sname,) not in result : 
        suserid = input("Enter site userid : ")
        spasswd = input("Enter site password : ")
        command = "insert into "+name+" values('{Site}','{Userid}','{Passwd}')".format(Site = sname, Userid = suserid, Passwd = spasswd)
        mycursor.execute(command)
        mydb.commit()
        print("Site successfully added!")
    else : 
        print("Site record already exists.")


def editsite(name):
    sname = input("\nEnter name of website : ")
    command = "select Site from "+name
    mycursor.execute(command)
    result = mycursor.fetchall()
    if (sname,) in result : 
        suserid = input("Enter new userid for site : ")
        spasswd = input("Enter new password for site : ")
        command = "update "+name+" set Userid = '"+suserid+"', Passwd = '"+spasswd+"' where Site = '"+sname+"'"
        mycursor.execute(command)
        mydb.commit()
        print("Site successfully edited!")
    else : 
        print("No record found for this site. Please add site first.")


def deletesite(name):
    sname = input("\nEnter name of website : ")
    command = "select Site from "+name
    mycursor.execute(command)
    result = mycursor.fetchall()
    if (sname,) in result :
        con = input("\nDeleting site "+sname+", please type 'delete' to confirm : ")
        if con == 'delete' :
            command = "delete from "+name+" where Site = '"+sname+"'"
            mycursor.execute(command)
            mydb.commit()
            print("Site successfully deleted.")
        else : 
            print("Deletion cancelled.")
    else : 
        print("No record found for this site.")


def main():
    cont = "yes"
    print("")
    print("----- WELCOME TO PASSWORDVAULT -----")
    print("This program will help you store your site information and passwords and manage them.")
    print("")
    print("Please note that all information is case sensitive, inlucding name of sites and usernames.")
    print("Hence, the program will treat 'gmail' and 'Gmail' as two separate sites.")
    print("")
    cont = input("Please type 'yes' to conitnue, or anything else to end the program : ")    
    while cont == "yes" :
        mycursor.execute("create table if not exists users(name varchar(25), masterpwd varchar(25))")
        mycursor.execute("select * from users")
        usersread = mycursor.fetchall()
        for each in usersread:
            key = each[0]
            value = each[1]
            users[key] = value
        print("")
        print("Here are your options : ")
        print("1. Add new user")
        print("2. Access information of an existing user, and add, delete or edit sites")
        print("3. Delete a user")
        print("4. Edit user's personal information")
        print("")
        i = input("Please enter the number corresponding to your choice : ")
        try : 
            choice = int(i)
            if choice == 1 : 
                createuser()
            elif choice == 2 : 
                accessexisting()
            elif choice == 3 : 
                deleteuser()
            elif choice == 4 :
                username = input("\nEnter user's name : ")
                edituser(username)
            else : 
                print("Invalid choice, please try again.")
        except : 
            print("Please type numbers from 1 to 4 only.")
        cont = input("\nPlease type 'yes' to continue or anything else to exit : ")
    print("\nThank you for using this program! Any suggestion, bugs or issues can be mailed to amanpaliwal543@gmail.com.")


main()
        
    
                


    




    
