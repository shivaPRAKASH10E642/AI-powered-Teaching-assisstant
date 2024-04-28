## with provided summary from the transcript, generate summary for the content, study plan and question and answers
from openai import OpenAI


# generate summary from provided text
def generate_summary_studyplan_QandA(text, api_key):
    user_prompt = (
        "provide summary, lesson plan and multiple choice questions to below context\n"
        + text
    )
    client = OpenAI(api_key=api_key)
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "you are a helpful teaching assistant, you will help teachers and students in generating summary, lesson plan and question and answers in multiple choice for the provided context.",
                "role": "user",
                "content": user_prompt,
            }
        ],
    )


if __name__ == "__main__":
    text = "You can now use AutoGen to create multiple AI agents to work together to complete a task that you defined. Let's take a look at what AutoGen is, and then I'll show you how to quickly start using it. AutoGen is a new framework by Microsoft, and it was announced at the end of September of two thousand twenty three. Its main goal is to simplify the orchestration, optimization, and automation of l l on workflows. Basically, it makes it very simple and flexible to create multiple agents, define their roles, and set them up to work together. All you have to do, if you follow their announcement blog post, is to define a set of agents with specialized capabilities and roles and also to define the interaction behavior between the agents. So it all sounds a little bit vague here or an abstract, but let's take a look at the code examples that they have for us, and then we'll have a better idea of how to use multiple agents together. As part of their GitHub repository, there is a nice documentation and example section for AutoGen. I will make sure to leave the link in the description for you if you wanna go ahead and follow along with the code. There are a bunch of different types of examples here. Today, I'm going to start with the automated task solving with code generation, execution, and the debugging example. So I just have, it copied on my own drive, on my Colab notebook. The first thing that we need to do, of course, is to install PyAutoGen, and they have, the code written for me. So that's something that I've already done. So we can move on. And next thing is to set up your configuration with OpenAI. How they manage to do this is by a config list file. So what you need to do is to create yourself a config OAI underscore config underscore list file. And in there, you're gonna specify the model that you want to use and your OpenAI API key. This is, part of my OpenAI API key. And then you can upload the file without any extensions to GitHub. One thing not GitHub. Sorry. Colab. One thing that I had trouble with was in this example here, they are they're only using single quote, quotation marks, but it expects the model expects it to be double quotation marks. So the code expects it to be the double quotation marks. So if you, use only the single ones, it's not going to work. So make sure when you're creating your file that it is a valid JSON file, plus it uses double quotation marks. Once that's done, we can set up the configuration. Things are gonna work well there. If you want, you can also set up configuration for other types of models. Today, I'm going to use GPT four. That's why, I'm only specifying the API key for GPT four. If it hasn't changed, by the way, last time I checked, you had to add some funds to your OpenAI account to be able to use g p t four. So make sure you have some funds on OpenAI. Otherwise, you might not be able to use this code. So when we are using AutoGen, the first thing that got my attention was that there are multiple different agent types. And in the simplest example, we have the assistant agent and we have the user proxy agent, and we are calling them initializing them through AutoGen. The assistant agent is basically the AI assistant. Like, when you're typing to chat GPT and the assistant that replies to you, that is going to be the assistant agent. The user proxy agent is the proxy for you. So instead of having a user, a human, you're going to have the user proxy agent, and it's going to act like a user. So let's go over the parameters to understand understand them a bit better. So we have the name for them. This is not consequential. It's just for us to understand who is talking when we're reading the conversation down below. You can so the assistant agent is going to answer the questions or answer in the chat chat based on an LLM, and that's why I want to set up a LLM configuration. So So we are setting it to config list, which is basically our OpenAI API key, the seed to make sure that the results are reproducible, and the temperature. And the configuration is basically very similar to, as they're saying here, or at least is compatible with the OpenAI API's configuration. So if there is a configuration you were using with the OpenAI API before, you can use it here too. And then let's take a look at the user proxy agent. Again, we pass it a name, and then there is something called the human input mode. So for the human input mode, you have three options. One of them is never, the other one is always, and the other one is terminate. This parameter specifies if this user proxy agent is going to wait for feedback or input from the actual human, which is the user, so us. If you say never, it's never going to wait for feedback or input from the user, from the human. If you say terminate, it's going to wait for a input from the user once the conversation is terminated, and I'm gonna talk about that in a second when that happens. Or you can say always in that case before the user proxy agent does anything, it's going to wait for an input from the user. But we want these agents to work together. So, obviously, we're going to set it to never so that they can do their job without us interfering. Then we set some termination limits. For example, one of them is max consecutive auto reply. So this agent will reply maximum of ten times, and then it's going to stop. Or another way to terminate this chat is for the assistant to send the message, terminate. So this is what we're doing here. We're checking what the message from the assistant is. If it is terminate, it is going to be the termination message for this chat. And then we have the code execution config. So this one specifies whether this agent is going to run the code or not. So what will we so what would happen if you were using chat g p t and ask you ask it to create some sort of code for you? It will create the code. You will take the code, paste it into, for example, Visual Studio Code, and then run it. And if there's an error, you would go back to ChatTPT and say, hey. The code didn't work. But instead, by setting the code execution config not false, you're saying that this user proxy agent can run the code by itself. So it's not going to ask for you to say to run it. It's going to run it by itself. And if there are any errors, it's going to return, those errors to the assistant agent so that the assistant agent can work on the code a bit more. And it's very straightforward and it's kind of common sense. The next thing that we need to do is for the user proxy agent to initiate the chat just like a human would by going to, a interface where they can have a chat with the AI agent, and it will send the assistant agent a message, and the message will be the task. Task is, what date is today? Compare the year to date gain for Meta and Tesla. So if we run this so that we can watch it happening from the beginning, The user proxy agent to the assistant says, what date is today compared to year to date gain for Meta and Tesla? The assistant says, first, let's get the current date using Python and then gives us some code. Next, we need to fetch the stock prices, and then, it tells you what it needs to do for that, which library it needs to use, which is y finance. Please install the library. If you haven't done so already, you can install it using the following command. Even tells you what, code to run, what pip command to run to install the library, and then gives you a bit more of a code. And then it's time for the proxy user and then it executes the code And then it says, hey. There's an error. The date is not defined. And then back to the assistant. I apologize for the oversight. Maybe if I close this, we can see it better. It seems there was an error because the date module was not imported. So it revises the code, sends it back to you. We execute it again, or the user proxy agent executes it again. There was another problem. I apologize for the confusion, says the assistant. It seems that the ticker symbol for the meta platforms changed from f b to meta, corrects it, sends it again, and then the user runs the code and is able to calculate the results. And then the assistant says, great. The code has executed successfully, and then it gives you the result, the answer to the question that you asked in the first place in a proper way, in a readable human readable way. And it says, as of today, the year to date gain for meta platforms is approximately hundred thirty seven point thirty seven percent, and for Tesla, it is approximately ninety point thirty four percent, and it gives a bit more of an analysis here. And once once it's done, it tells us to terminate. In my opinion, this is amazing that these models can just work together and solve problems and actually give you the answer that you're looking for. In the rest of this notebook, there are actually a bunch more examples of them creating some, plot and then saving that plot on a file. So if you wanna go further with it, of course, definitely go ahead. I think it's very interesting. So this is a chart that they create. But, to not make this video very long, I actually wanna show you another example with three, agents. So, again, what we need to do is install, PyAutoGen, of course, and then make sure the configuration is set up. Yeah. Nice that my run time wasn't reset. So like before, I again uploaded the OAI OAI config list here. So, basically, how it works here is that we have three agents working together. We have a coder, so like before, someone who prepares the code. We have the user proxy, so someone who acts in behalf of the human. And then we have a vis critic, so visual visualization critic. So what the task is here, we ask the coder to write the code to generate a visualization, which is the the user proxy asks for it. And then the vis critic, the visualization critic, gives some feedback. So let's see how we set this up. So we they set up the in the example, they set up the LOM config here, but, you know, it could also just like before, it can just be in the coder assistant agent's, definition. The user proxy is more or less the same. We give it a name. There is a system message that says that you are a human admin. You don't have to pass a system, message. You only have to do it if you wanna specify something, in detail that you want the user proxy agent to do. And there is a code execution config. And then, again, we say human input mode is never. For the coder, we again pass it a name and a LLM config because it's going to be using a large language model to generate the code. And the more interesting one here is the critic. So we pass it the name, but then we pass it a really long system message. And in this one, we are basically prompting it to take a look at a bunch of things and then write rate the visualization that was created. So we say, critic, you are a helpful assistant, highly skilled in evaluating the quality of a given visualization code by providing a score from one to ten. And then we also give it we also pass it some criteria. So whether there are any bugs, how was the data transformation, the goal compliance, how well the code meets the specified visualization goals, visualization type, data encoding, aesthetics, and so on and so forth. It even says you must provide a score for each of the above dimensions. And then, again, we pass it the LLM config because, again, it's going to depend on a large language model to give the answers as opposed to the user proxy agent, which only runs a code that was provided to it. Differently than from last time, they have a group chat component, and that's the one that we're going to use. So we create a group chat. We pass all the agents that's that are going to be in this group chat. We specify the termination limit to be twenty, so there is going to be a maximum of twenty rounds. And then we create a manager using this group chat configuration. And then, again, user proxy initiates the chat by sending a message to the group chat, and the message is download the data from this link, and then plot a visualization that tells us about the relationship between weight and horsepower. Let's make it a bit bigger so it's a bit more readable. And then let's take a look at the conversation that took place. So the user proxy, again, prompts the chat as we mentioned. And then the coder says, alright. Here are the steps we're going to follow. And then it gives you step by step what it's going to do. And then it creates the code and all the PIP installs that we need to do. And then it says you can save the above transcript in a Python file named download and plot dot py and run it. And then a plot will be saved on this PNG. The critic says there are no bugs. Information is good. Compliance is good. Encoding can be better, and the aesthetics can be better. And then to improve the code, it gives the assistant some pointers. And then the coder says, thanks for the feedback. I'll add grid lines to the plot along with a color gradient based on a density of points for better representation, and then updates the code. The critic comes back again, and looks like the aesthetics points are better now. And then it says still there can be some improvements with encoding. And then our user proxy executes the code, and the coder says, oh, there are some problems, updates the code, runs again. And as you can see, it's a very involved conversation between three agents of working together to create the best code possible, to plot a dataset, which is extremely impressive, in my opinion. If you wanna take a look at more of the examples, I will, like I said, make sure to, have the link in the description for all the examples. And there is some really good documentation that will help you understand how to use the group chat option, how to use different types of, agents here, and, overall, make use of this library to maybe even automate some of your work, which I think would be very cool. I hope this was helpful. If you have any questions, don't forget to leave a count comment below. And if you want more advanced tutorials on AutoGen, also let us know. Maybe we can take some time to create something custom and then, work on that and I'll share that with you. Thanks for watching, and I will see you in the next video"