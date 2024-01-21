from openai import OpenAI
import prompts
import json
import os

from dotenv import load_dotenv
load_dotenv()

client = OpenAI()

class Model:
    """
    Base model class for handling responses from GPT models.
    """
    def __init__():
        pass
    
    def response_to_json(self, response):
        # Defined helper function
        def valid_json(response):
            return isinstance(response, (list, dict))
        
        # First, check if the current response is already a JSON object 
        # (list or dictionary). If it is, return directly
        if valid_json(response):
            print("Good output already")
            return response
        # elif "```json" in response:
        #     print("Reading through GPT4's template")
        #     components = response.split("```")
        #     formatted_response = components[1].split("json")[-1].strip()
        #     json_response = (formatted_response 
        #                         if isinstance(formatted_response, (list, dict)) 
        #                         else json.loads(formatted_response))
        #     assert(valid_json(json_response)), "Failed validating JSON"
            
        #     return json_response

        # If not, you should feed the response to GPT3.5 
        else:
            print("Feed through another agent for formatting")
            # Outline the two applicable models
            gpt_4_model = "gpt-4-1106-preview"
            gpt_3_model = "gpt-3.5-turbo-1106"
            
            gpt_response = client.chat.completions.create(
                model=gpt_3_model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": prompts.json_system_string},
                    {"role": "user", "content": prompts.json_prompt_string.format(response)}
                ],
            )
            formatted_response = gpt_response.choices[0].message.content
            json_response = (formatted_response 
                                if isinstance(formatted_response, (list, dict)) 
                                else json.loads(formatted_response))
            assert(valid_json(json_response)), "Failed validating JSON"
            
            return json_response
        
class VisionModel(Model):
    """
    A model class for handling vision-related tasks with GPT models.
    """
    def __init__(self):
        self.model_name = "gpt-4-vision-preview"
    
    def get_image_url(self, image):
        if image.startswith("http"):
            return {"url": image}
        elif isinstance(image, str):
            return {"url": f"data:image/jpeg;base64,{image}"}
        else:
            raise ValueError("Invalid type for image. It should be either a URL or a base64 encoding.")
        
    def get_image_dict(self, image_src, detail=None):
        image_url = self.get_image_url(image_src)
        if detail:
            image_url.update({"detail":detail})
        image_dict = {"type": "image_url", "image_url": image_url}
        return image_dict
    
    def gpt_call(self, messages, validator=None, json_output=True, error_fn=None):
        print(messages)
        # Runs the visual critique component
        vision_response = client.chat.completions.create(
            model=self.model_name,
            messages=messages,
            max_tokens=4096,
        )
        chat_response = vision_response.choices[0].message.content
        print(chat_response)
        
        if json_output:
            json_response = self.response_to_json(chat_response)
            # If we have a validator and we have failed it, return the chat
            if validator and not validator(json_response):
                if error_fn:
                    return error_fn(chat_response)
                else:
                    return {"error": chat_response}
            # Otherwise, return the json response
            else:
                return json_response
        else:
            return chat_response

class CompareGPT(VisionModel):
    """
    A class to compare two UI screenshots using GPT models.
    """
    def get_comparison_message(self, source_image_src, target_image_src, detail=None):
        """
        Prepares the message payload for comparing two UI screenshots.

        Args:
            source_image_src (str): URL or base64 string of the source image.
            target_image_src (str): URL or base64 string of the target image.
            detail (str, optional): Level of detail for the comparison.

        Returns:
            list: A list of messages to be sent to the GPT model.
        """
        # Render the system and text dictionaries
        system = {"role": "system", "content": prompts.comp_vision_system_string}
        text = {"type": "text", "text": prompts.comp_vision_prompt_string}
        
        # Render the image dictionary
        # source_image_url = self.get_image_url(source_image_src).update({"detail": detail}) if detail else self.get_image_url(source_image_src)
        # target_image_url = self.get_image_url(target_image_src).update({"detail": detail}) if detail else self.get_image_url(target_image_src)
        # source_image = {"type": "image_url", "image_url": source_image_url}
        # target_image = {"type": "image_url", "image_url": target_image_url}
        
        # TODO: Converge to these more efficient implementations
        source_image = self.get_image_dict(source_image_src)
        target_image = self.get_image_dict(target_image_src)
        
        # Render the user
        user = {"role": "user", "content": [text, source_image, target_image]}
        
        # Render the messages
        messages = [system, user]
        
        # Return the messages
        return messages
    
    def validator(self, output):
        return (
            isinstance(output, dict)
            and ("score" in output)
            and ("feedback" in output)
            and isinstance(output['feedback'], list)
        )
        
    def format_error_response(self, chat_response):
        return {
            "score": 0,
            "feedback": [chat_response]
        }

    def forward(self, source_image_src, target_image_src, detail="high"):
        message = self.get_comparison_message(source_image_src, target_image_src, detail=detail)
        return self.gpt_call(message, validator=self.validator, error_fn=self.format_error_response)
    
class EvalGPT(VisionModel):
    """
    A class to evaluate a UI screenshot based on standard UI principles.
    """
    def get_standard_message(self, image, detail=None):
        """
        Prepares the message payload for evaluating a UI screenshot.

        Args:
            image (str): The image to be evaluated.
            detail (str, optional): Level of detail for the evaluation.

        Returns:
            list: A list of messages to be sent to the GPT model.
        """
        # Render the system and text dictionaries
        system = {"role": "system", "content": prompts.ui_evaluation_system_string}
        text = {"type": "text", "text": prompts.ui_evaluation_prompt_string}
        
        # Render the image dictionary
        # image_url = self.get_image_url(image).update({"detail": detail}) if detail else self.get_image_url(image)
        # image = {"type": "image_url", "image_url": image_url}
        image = self.get_image_dict(image)
        
        # Render the user
        user = {"role": "user", "content": [text, image]}
        
        # Render the messages
        messages = [system, user]
        
        # Return the messages
        return messages
    
    def validator(self, output):
        return (
            isinstance(output, dict)
            and ("Navigation" in output)
            and (len(output['Navigation']) == 2)
            and isinstance(output['Navigation'][0], int)
            and isinstance(output['Navigation'][1], str)
        )
        
    def format_error_response(self, chat_response):
        return {
            "Navigation" : [0, chat_response],
            "Aesthetics" : [0, chat_response],
            "Usability" : [0, chat_response],
            "Consistency" : [0, chat_response],
        }
    
    def forward(self, image_src, detail="high"):
        message = self.get_standard_message(image_src, detail=detail)
        return self.gpt_call(message, validator=self.validator, error_fn=self.format_error_response)
    
class UserEvalGPT(VisionModel):
    """
    A class to evaluate a UI screenshot based on user-defined priorities.
    """
    def get_custom_message(self, image, priorities, detail=None):
        """
        Prepares the message payload for evaluating a UI screenshot based on user-defined priorities.

        Args:
            image (str): The image to be evaluated.
            priorities (list): A list of user-defined priorities for the evaluation.
            detail (str, optional): Level of detail for the evaluation.

        Returns:
            list: A list of messages to be sent to the GPT model.
        """
        # Render the system and text dictionaries
        system = {"role": "system", "content": prompts.vision_system_string}
        text = {"type": "text", "text": prompts.vision_prompt_string.format(priorities)}
        
        # Render the image dictionary
        # image_url = self.get_image_url(image).update({"detail": detail}) if detail else self.get_image_url(image)
        # image = {"type": "image_url", "image_url": image_url}
        image = self.get_image_dict(image)
        
        # Render the user
        user = {"role": "user", "content": [text, image]}
        
        # Render the messages
        messages = [system, user]
        
        # Return the messages
        return messages

    def forward(self, image_src, priorities, detail="high"):
        message = self.get_custom_message(image_src, priorities, detail=detail)
        return self.gpt_call(message)
