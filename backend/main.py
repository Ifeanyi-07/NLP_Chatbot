from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
import db_helper
import generic_helper


app= FastAPI()


inprogress_orders = {}


def new_order(parameters, session_id: str):

    inprogress_orders.pop(session_id, None)

    return JSONResponse(content={
        "fulfillmentText": "Sure! Let's start a new order. What would you like to order?. Specify food items and quantities. For example, you can say, 'I would like to order two pizzas and one Jollof rice'. Also, we have only the following items on our menu: Jollof rice, Chicken sausage and potato skillet, Pizza, Ground turkey stuffed bell peppers, Crockpot black eyed peas, Dutch oven chicken pot pie, Beef stew with onion soup mix, Authentic Nigerian fried rice, and Samosa."
    })


def add_to_order(parameters, session_id: str):
    food_items = parameters['food-item']
    quantities = parameters['number1']

    if len(food_items) != len(quantities):
        fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities clearly?"
    else:
        new_food_dict = dict(zip(food_items, quantities))

        if session_id in inprogress_orders:
            current_food_dict = inprogress_orders[session_id]
            current_food_dict.update(new_food_dict)
            inprogress_orders[session_id] = current_food_dict
        else:
            inprogress_orders[session_id] = new_food_dict

        order_str = generic_helper.get_str_from_food_dict(inprogress_orders[session_id])
        fulfillment_text = f"So far you have: {order_str}. Do you need anything else?"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })

def complete_order(parameters, session_id: str):
    if session_id not in inprogress_orders:
        fulfillment_text = "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
    else:
        order= inprogress_orders[session_id]
        order_id= save_to_db(order)

        if order_id == -1:
            fulfillment_text = "Sorry, I couldn't process your order due to a backend error. " \
                               "Please place a new order again"
        else:
            order_total = db_helper.get_total_order_price(order_id)

            fulfillment_text = f"Awesome. We have placed your order. " \
                               f"Here is your order id: #{order_id}. " \
                               f"Your order total is ${order_total} which you can pay Online or at the time of delivery!"

        del inprogress_orders[session_id]

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def save_to_db(order):
    next_order_id = db_helper.get_next_order_id()

    for food_item, quantity in order.items():
        rcode= db_helper.insert_order_item(food_item, quantity, next_order_id)

        if rcode == -1:
            return -1

    # Now insert order tracking status
    db_helper.insert_order_tracking(next_order_id, "in progress")

    return next_order_id

# def remove_from_order(parameters, session_id: str):
#         if session_id not in inprogress_orders:
#             return JSONResponse(content={
#                 "fulfillmentText": "I'm having a trouble finding your order. Sorry! Can you place a new order please?"
#             })
#
#         current_order = inprogress_orders[session_id]
#         food_items = parameters["food-item"]
#
#         removed_items = []
#         no_such_items = []
#
#         for item in food_items:
#             if item not in current_order:
#                 no_such_items.append(item)
#             else:
#                 removed_items.append(item)
#                 del current_order[item]
#
#         if len(removed_items) > 0:
#             fulfillment_text = f'Removed {",".join(removed_items)} from your order!'
#         if len(no_such_items) > 0:
#             fulfillment_text = f' Your current order does not have {",".join(no_such_items)}'
#         if len(current_order.keys()) == 0:
#             fulfillment_text += " Your order is empty!"
#         else:
#             order_str = generic_helper.get_str_from_food_dict(current_order)
#             fulfillment_text += f" Here is what is left in your order: {order_str}. Anything else?"
#
#         return JSONResponse(content={
#             "fulfillmentText": fulfillment_text
#         })
def remove_from_order(parameters, session_id: str):
    if session_id not in inprogress_orders:
        return JSONResponse(content={
            "fulfillmentText": "I'm having trouble finding your order. Sorry! Can you place a new order please?"
        })

    current_order = inprogress_orders[session_id]

    food_items = parameters.get("food-item", [])
    quantities = parameters.get("number", [])

    # Make sure values are lists
    if not isinstance(food_items, list):
        food_items = [food_items]

    if not isinstance(quantities, list):
        quantities = [quantities]

    removed_items = []
    no_such_items = []

    for i, item in enumerate(food_items):

        # Item doesn't exist in current order
        if item not in current_order:
            no_such_items.append(item)
            continue

        # Check whether a quantity was specified
        if i < len(quantities) and quantities[i] not in ("", None):
            quantity_to_remove = int(quantities[i])

            current_quantity = current_order[item]

            # Requested quantity is greater than or equal to
            # the quantity currently in the order
            if quantity_to_remove >= current_quantity:
                del current_order[item]

                removed_items.append(
                    f"{item} (all {current_quantity})"
                )

            else:
                current_order[item] -= quantity_to_remove

                removed_items.append(
                    f"{quantity_to_remove} {item}"
                )

        # No quantity specified → remove the whole item
        else:
            current_quantity = current_order[item]

            del current_order[item]

            removed_items.append(
                f"{item} (all {current_quantity})"
            )

    # Build response
    response_parts = []

    if removed_items:
        response_parts.append(
            f"Removed {', '.join(removed_items)} from your order!"
        )

    if no_such_items:
        response_parts.append(
            f"Your current order does not have {', '.join(no_such_items)}."
        )

    # Check if order is now empty
    if len(current_order) == 0:
        response_parts.append("Your order is empty!")
    else:
        order_str = generic_helper.get_str_from_food_dict(current_order)

        response_parts.append(
            f"Here is what is left in your order: {order_str}. Anything else?"
        )

    fulfillment_text = " ".join(response_parts)

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def track_order(parameters, session_id: str):
    order_id = int(parameters['number'])
    order_status = db_helper.get_order_status(order_id)

    if order_status:
        fulfillment_text = f"The order status for order id #{order_id} is:  {order_status.upper()}"
    else:
        fulfillment_text = f"No order found for order id: {order_id}"

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


@app.post("/")
async def handle_request(request: Request):

    # Retrieve the JSON data from the request
    payload = await request.json()

    # Extract the necessary information from the payload
    intent = payload['queryResult']['intent']['displayName']
    parameters = payload['queryResult']['parameters']
    output_contexts = payload['queryResult']['outputContexts']

    session_id= generic_helper.extract_session_id(output_contexts[0]["name"])

    intent_handler_dict = {
        'add_order - context: ongoing-order': add_to_order,
        'new_order': new_order,
        'remove_order - context: ongoing-order': remove_from_order,
        'complete_order - context: ongoing-order': complete_order,
        'track_order - context: ongoing-tracking': track_order
    }

    return intent_handler_dict[intent](parameters, session_id)