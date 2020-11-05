# -*- coding: utf-8 -*-

# by D. James Smith

import requests
import boto3
import json
import datetime
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

FEELINGS = "None"
SLEEP = "None"
HOURS = ""
SYMPTOMS = "None"
BRUSQUE = "None"
DATETIME = datetime.datetime.now().strftime("%b %d %Y %H:%M")
URL = "https://cs5500-healthcare.herokuapp.com/v1/alexa"

turns = ["brusqueIntent","feelingsIntent","sleepIntent","hoursSleptIntent","symptomIntent"]
TURN = -1

class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("LaunchRequest")(handler_input) 

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        global TURN
        TURN = turns.index("feelingsIntent") # 1
        speak_output = "How are you feeling?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class feelingsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("feelingsIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        global FEELINGS
        global TURN
        TURN = turns.index("sleepIntent") # 2
        slots = handler_input.request_envelope.request.intent.slots
        FEELINGS = slots["feelings"].value
        speak_output = "How many hours did you sleep?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class sleepIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("sleepIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        global SLEEP
        global TURN
        TURN = turns.index("hoursSleptIntent") # 3
        slots = handler_input.request_envelope.request.intent.slots
        SLEEP = slots["sleep"].value
        speak_output = "How many hours did you sleep?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class hoursSleptIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("hoursSleptIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        global HOURS
        global TURN
        TURN = turns.index("symptomIntent") # 4
        slots = handler_input.request_envelope.request.intent.slots
        HOURS = slots["amount"].value
        speak_output = "What symptoms do you have?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class symptomIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("symptomIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        global FEELINGS
        global SLEEP
        global HOURS
        global SYMPTOMS
        global DATETIME
        global URL
        global TURN 
        TURN = -1
        slots = handler_input.request_envelope.request.intent.slots
        SYMPTOMS = slots["symptoms"].value
        # get device id
        sys_object = handler_input.request_envelope.context.system
        device = sys_object.device.device_id
        PARAMS = {"feelings":FEELINGS,"hours":HOURS,"symptoms":SYMPTOMS,"time":DATETIME,"device":device}
        #r = requests.get(url=URL,params=PARAMS)
        r = requests.post(url=URL,data=json.dumps(PARAMS),headers={'Content-Type':'application/json'})
        speak_output = "Thank you for participating. Status code %d" % (r.status_code)
        #speak_output = "You have reported that you feel {0}, you slept {1}, and you have {2}. Thank you for participating.".format(FEELINGS,SLEEP,SYMPTOMS)
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class brusqueIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("brusqueIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        global FEELINGS
        global SLEEP
        global HOURS
        global SYMPTOMS
        global DATETIME
        global URL
        global TURN 
        global BRUSQUE
        slots = handler_input.request_envelope.request.intent.slots
        BRUSQUE = slots["brusque"].value
        if TURN==1:
            TURN = 2
            FEELINGS = BRUSQUE
            speak_output = "How many hours did you sleep?"
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    # .ask("add a reprompt if you want to keep the session open for the user to respond")
                    .response
            )
        elif TURN==2:
            TURN = 3
            SLEEP = BRUSQUE
            speak_output = "How many hours did you sleep?"
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    # .ask("add a reprompt if you want to keep the session open for the user to respond")
                    .response
            )
        elif TURN==3:
            TURN = 4
            HOURS = BRUSQUE
            speak_output = "What symptoms do you have?"
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    # .ask("add a reprompt if you want to keep the session open for the user to respond")
                    .response
        )
        elif TURN==4:
            TURN = -1
            SYMPTOMS = BRUSQUE
            # get device id
            sys_object = handler_input.request_envelope.context.system
            device = sys_object.device.device_id
            PARAMS = {"feelings":FEELINGS,"hours":HOURS,"symptoms":SYMPTOMS,"time":DATETIME,"device":device}
            #r = requests.get(url=URL,params=PARAMS)
            r = requests.post(url=URL,data=json.dumps(PARAMS),headers={'Content-Type':'application/json'})
            speak_output = "Thank you for participating. Status code %d" % (r.status_code)
            #speak_output = "You have reported that you feel {0}, you slept {1}, and you have {2}. Thank you for participating.".format(FEELINGS,SLEEP,SYMPTOMS)
            return (
                handler_input.response_builder
                    .speak(speak_output)
                    # .ask("add a reprompt if you want to keep the session open for the user to respond")
                    .response
            )
        speak_output = "That was a brusk intent"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )

class HelloWorldIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("HelloWorldIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Hello World!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(feelingsIntentHandler())
sb.add_request_handler(sleepIntentHandler())
sb.add_request_handler(hoursSleptIntentHandler())
sb.add_request_handler(symptomIntentHandler())
sb.add_request_handler(brusqueIntentHandler())
sb.add_request_handler(HelloWorldIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
