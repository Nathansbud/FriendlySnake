import discord
import os
import json
from datetime import date
from random import randint

with open(os.path.join(os.path.dirname(__file__), "credentials" + os.sep + "discord.json")) as jf:
    creds = json.load(jf)

todo_path = os.path.dirname(__file__) + os.sep + "data" + os.sep + "todo.json"
client = discord.Client()

def generate_id():
    return str(randint(10000000, 99999999))

async def update_todo():
    c = client.get_channel(614850532493885451)
    try:
        msg = await c.fetch_message(c.last_message_id)
        await msg.delete()
    except discord.errors.NotFound:
        pass

    await c.send(get_todo_print())

def get_todo_print(opts=[]):
    out = ""
    count = 1
    with open(todo_path) as jf:
        todo = json.load(jf)

    for item in todo['current_tasks']:
        out += str(count) + ") " + \
               (item['task'] + " " if "task" in item else "") + \
               (("[Assigned: " + item['assigned'] + "] ") if "assigned" in item else "") + \
               (("[Committee: " + item['committee'] + "] ") if "committee" in item else "") + \
               (("[Due: " + item['due'] + "] ") if "due" in item else "") + \
               (("[Added: " + item['date'] + " by " + item['author'] + "] ") if "showadded" in opts else "") + \
               ("[ID: " + item['id'] + "] ") + "\n"
        count += 1
    return out

@client.event
async def on_ready():
    print(str(client.user) + " has logged in")

@client.event
async def on_message(message):
    global client

    ml = message.content.lower()

    if ml.startswith("$addtask ") or ml.startswith("$add ") or ml.startswith("$additem ") or ml.startswith("$edit "):
        if ml.strip() == "$addtask" or ml.strip() == "$add" or ml.strip() == "$additem" or ml.strip() == "$edit":
            pass
        else:
            is_edit = ml.startswith("$edit ")
            task_parts = [part for part in message.content.split("$") if len(part) > 0]
            task_dict = {
                "date": date.today().strftime("%m/%d"),
                "author": message.author.display_name,
            }
            if is_edit:
                t_id = task_parts[0][task_parts[0].find(" ")+1:].strip()
                passed = False
                with open(todo_path, 'r+') as jf:
                    load_tasks = json.load(jf)
                    for item in load_tasks['current_tasks']:
                        if t_id == item['id']:
                            task_dict = item
                            passed = True
                if not passed:
                    await message.channel.send("No task with ID currently in todo list!")
                    return True
            for part in task_parts:
                p = part.lower()

                if p.startswith("task ") or p.startswith("add ") or p.startswith("additem ") or p.startswith("addtask "):
                    task_dict["task"] = part[part.find(" ")+1:].strip()
                elif p.startswith("for ") or p.startswith("assigned ") or p.startswith("responsible "):
                    task_dict["assigned"] = part[part.find(" ")+1:].strip()
                elif p.startswith("by ") or p.startswith("due "):
                    task_dict["due"] = part[part.find(" ")+1:].strip()
                elif p.startswith("author ") or p.startswith("from "):
                    task_dict["author"] = part[part.find(" ")+1:].strip()
                elif p.startswith("committee ") or p.startswith("group "):
                    task_dict["committee"] = part[part.find(" ")+1:].strip()

            if "task" in task_dict and len(task_dict['task']) != 0:
                with open(todo_path, 'r+') as jf:
                    load_tasks = json.load(jf)
                    if is_edit:
                        for item in load_tasks['current_tasks']:
                            if item['id'] == task_dict['id']:
                                load_tasks['current_tasks'].remove(item)
                                load_tasks['current_tasks'].append(task_dict)
                                jf.seek(0)
                                json.dump(load_tasks, jf, indent=4)
                                jf.truncate()
                        await message.channel.send("Edited task '" + task_dict['task'] + "' [ID: " + task_dict['id'] + "]!")
                    else:
                        ids = [t['id'] for t in (load_tasks['current_tasks'] + load_tasks['completed_tasks']) if'id' in t]

                        task_dict['id'] = generate_id()
                        while task_dict['id'] in ids:
                            task_dict['id'] = generate_id()

                        load_tasks['current_tasks'].append(task_dict)
                        jf.seek(0)
                        json.dump(load_tasks, jf, indent=4)
                        jf.truncate()

                        await message.channel.send("Added task '" + task_dict['task'] + "' [ID: " + task_dict['id'] + "] to the to-do list!")
                await update_todo()
            else: await message.channel.send("Todo items must have a task! Try again!")
    if ml.startswith("$todo ") or ml == "$todo":
        out = get_todo_print([item.lower().strip() for item in message.content.split("-")[1:]])
        if len(out) > 0: await message.channel.send(out)
        else: await message.channel.send("No current items on the to-do list! Try adding one with $add!")
    if ml.startswith("$remove ") or ml.startswith("$delete "):
        m_id = message.content.split(" ")[1]
        passed = False
        with open(todo_path, "r+") as jf:
            todo = json.load(jf)
            for item in todo['current_tasks']:
                if item['id'] == m_id:
                    todo['current_tasks'].remove(item)
                    jf.seek(0)
                    json.dump(todo, jf, indent=4)
                    jf.truncate()
                    passed = True
        if passed:
            await message.channel.send("Deleted item " + m_id + " from todo list!")
            await update_todo()
        else: await message.channel.send("No item with ID " + m_id + " currently on the todo list!")

    if ml.startswith("$finish ") or ml.startswith("$complete "):
        m_id = message.content.split(" ")[1]
        passed = False

        with open(todo_path, "r+") as jf:
            todo = json.load(jf)
            for item in todo['current_tasks']:
                if item['id'] == m_id:
                    todo['current_tasks'].remove(item)
                    item['completed'] = date.today().strftime("%m/%d")
                    todo['completed_tasks'].append(item)
                    jf.seek(0)
                    json.dump(todo, jf, indent=4)
                    jf.truncate()
                    passed = True

        if passed:
            await message.channel.send("Added item with ID " + m_id + " to completed task list!")
            await update_todo()
        else: await message.channel.send("No item with ID " + m_id + " currently on the todo list!")

    if ml.startswith("$completed ") or ml.startswith("$finished ") or ml == "$completed" or ml == "$finished":
        with open(todo_path) as jf:
            todo = json.load(jf)
        count = 1
        out = ""
        for item in todo['completed_tasks']:
            out += str(count) + ") " + \
                   (item['task'] + " " if "task" in item else "") + \
                   (("[Assigned: " + item['assigned'] + "] ") if "assigned" in item else "") + \
                   (("[Committee: " + item['committee'] + "] ") if "committee" in item else "") + \
                   ("[Completed: " + item['completed']+"] " if 'completed' in item else "")+\
                   ("[ID: " + item['id'] + "] ") + "\n"
            count += 1
        if len(out) > 0: await message.channel.send(out)
        else: await message.channel.send("No items have been completed! Mark a task as completed through $finish {ID}")

    if ml.startswith("$readd ") or ml.startswith("$return "):
        m_id = message.content.split(" ")[1]
        passed = False

        with open(todo_path, "r+") as jf:
            todo = json.load(jf)
            for item in todo['completed_tasks']:
                if item['id'] == m_id:
                    todo['completed_tasks'].remove(item)
                    item.pop('completed')
                    todo['current_tasks'].append(item)
                    jf.seek(0)
                    json.dump(todo, jf, indent=4)
                    jf.truncate()
                    passed = True

        if passed:
            await message.channel.send("Re-added item with ID " + m_id + " to current task list!")
        else: await message.channel.send("No item with ID " + m_id + " on the completed task list!")

client.run(creds['TBot']['bot_token'])

if __name__ == '__main__':
    pass
