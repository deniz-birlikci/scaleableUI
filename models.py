from openai import OpenAI
import prompts
import json

client = OpenAI()

class Model:
    def __init__():
        pass
    
    def response_to_json(self, response):
        # Defined helper function
        def valid_json(response):
            return isinstance(response, (list, dict))
        
        # First, check if the current response is already a JSON object 
        # (list or dictionary). If it is, return directly
        if valid_json(response):
            return response
        
        # If not, you should feed the response to GPT3.5 
        else:
            # Outline the two applicable models
            gpt_4_model = "gpt-4-1106-preview"
            gpt_3_model = "gpt-3.5-turbo-1106"
            
            gpt_response = client.chat.completions.create(
                model=gpt_4_model,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": prompts.json_system_string},
                    {"role": "user", "content": prompts.json_prompt_string.format(response)}
                ],
            )
            formatted_response = gpt_response['choices'][0]['message']['content']
            json_response = (formatted_response 
                                if isinstance(formatted_response, (list, dict)) 
                                else json.loads(formatted_response))
            assert(valid_json(json_response)), "Failed validating JSON"
            
            return json_response
        
class VisionModel(Model):
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
            image_url.expend({"detail":detail})
        image_dict = {"type": "image_url", "image_url": image_url}
        return image_dict
    
    def gpt_call(self, messages, json_output=True):
        # Runs the visual critique component
        vision_response = client.chat.completions.create(
            model=self.model_name,
            messages=messages
        )
        chat_response = vision_response['choices'][0]['message']['content']
        
        if json_output:
            return self.response_to_json(chat_response)
        else:
            return chat_response

class CompareGPT(VisionModel):
    def get_comparison_message(self, source_image_src, target_image_src, detail=None):
        # Render the system and text dictionaries
        system = {"role": "system", "content": prompts.comp_vision_system_string}
        text = {"type": "text", "text": prompts.comp_vision_prompt_string}
        
        # Render the image dictionary
        source_image_url = self.get_image_url(source_image_src).extend({"detail": detail}) if detail else self.get_image_url(source_image_src)
        target_image_url = self.get_image_url(target_image_src).extend({"detail": detail}) if detail else self.get_image_url(target_image_src)
        source_image = {"type": "image_url", "image_url": source_image_url}
        target_image = {"type": "image_url", "image_url": target_image_url}
        
        # TODO: Converge to these more efficient implementations
        # source_image = self.get_image_dict(source_image_src)
        # target_image = self.get_image_dict(target_image_src)
        
        # Render the user
        user = {"role": "user", "content": [text, source_image, target_image]}
        
        # Render the messages
        messages = [system, user]
        
        # Return the messages
        return messages

    def forward(self, source_image_src, target_image_src, detail="high"):
        message = self.get_comparison_message(source_image_src, target_image_src, detail=detail)
        return self.gpt_call(message)
    
class EvalGPT(VisionModel):
    def get_standard_message(self, image, detail=None):
        # Render the system and text dictionaries
        system = {"role": "system", "content": prompts.ui_evaluation_system_string}
        text = {"type": "text", "text": prompts.ui_evaluation_prompt_string}
        
        # Render the image dictionary
        image_url = self.get_image_url(image).extend({"detail": detail}) if detail else self.get_image_url(image)
        image = {"type": "image_url", "image_url": image_url}
        
        # Render the user
        user = {"role": "user", "content": [text, image]}
        
        # Render the messages
        messages = [system, user]
        
        # Return the messages
        return messages
    
    def forward(self, image_src, detail="high"):
        message = self.get_standard_message(image_src, detail=detail)
        return self.gpt_call(message)
    
class UserEvalGPT(VisionModel):
    def get_custom_message(self, image, priorities, detail=None):
        # Render the system and text dictionaries
        system = {"role": "system", "content": prompts.vision_system_string}
        text = {"type": "text", "text": prompts.vision_prompt_string.format(priorities)}
        
        # Render the image dictionary
        image_url = self.get_image_url(image).extend({"detail": detail}) if detail else self.get_image_url(image)
        image = {"type": "image_url", "image_url": image_url}
        
        # Render the user
        user = {"role": "user", "content": [text, image]}
        
        # Render the messages
        messages = [system, user]
        
        # Return the messages
        return messages

    def forward(self, image_src, priorities, detail="high"):
        message = self.get_custom_message(image_src, priorities, detail=detail)
        return self.gpt_call(message)
