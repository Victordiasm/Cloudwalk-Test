# Cloudwalk - Quality Engineering test

## 1. Introduction

Quality Engineering test for Cloudwalker.

## 2. Choiches in the project

- By now, we'll be using the name in the moment of the killing for kill record, even if the player change names.
    - This choice was made because updating the name of the player difficults keeping track of the player if he leaves and another one takes his ID. 
    - Ideal case would be logging players by more than one value, as IP, machine-name, a hash given by the client, etc.

## 3. Usage

 -Report.py
    - Takes the path of the log file as argument.
