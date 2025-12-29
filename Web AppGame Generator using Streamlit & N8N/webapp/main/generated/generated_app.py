import streamlit as st

# Initialize session state for groceries and cart if not already present
if 'groceries' not in st.session_state:
    st.session_state.groceries = {
        'Apple': {'quantity': 10, 'price': 1.50},
        'Banana': {'quantity': 15, 'price': 0.75},
        'Milk': {'quantity': 5, 'price': 3.00},
        'Bread': {'quantity': 8, 'price': 2.25},
        'Eggs': {'quantity': 12, 'price': 2.50},
        'Cheese': {'quantity': 7, 'price': 5.00},
        'Yogurt': {'quantity': 10, 'price': 1.20},
        'Chicken': {'quantity': 6, 'price': 8.00},
        'Rice': {'quantity': 20, 'price': 4.00},
        'Pasta': {'quantity': 18, 'price': 1.75},
    }

if 'cart' not in st.session_state:
    st.session_state.cart = {}

if 'total_price' not in st.session_state:
    st.session_state.total_price = 0.0

if 'purchase_history' not in st.session_state:
    st.session_state.purchase_history = []

if 'current_view' not in st.session_state:
    st.session_state.current_view = 'customer' # 'customer' or 'owner'

# Function to display customer view
def customer_view():
    st.title(" Groceries Supermarket")

    search_query = st.text_input("Search for an item:")

    st.subheader("Available Groceries:")
    col1, col2, col3 = st.columns([3, 1, 1])
    col1.write("**Item**")
    col2.write("**Qty**")
    col3.write("**Price**")
    st.markdown("---")

    displayed_items = {}
    for item, details in st.session_state.groceries.items():
        if search_query.lower() in item.lower():
            displayed_items[item] = details
            c1, c2, c3 = st.columns([3, 1, 1])
            c1.write(item)
            c2.write(details['quantity'])
            c3.write(f"${details['price']:.2f}")

    if not displayed_items:
        st.info("No items found matching your search.")

    st.markdown("---")

    st.subheader("Add to Cart:")
    selected_item = st.selectbox("Select an item to add to cart:", [""] + list(displayed_items.keys()), key="select_item")

    if selected_item:
        if selected_item not in st.session_state.groceries:
            st.error("Item not available.")
        else:
            item_details = st.session_state.groceries[selected_item]
            st.write(f"You selected **{selected_item}** (Available: {item_details['quantity']}, Price: ${item_details['price']:.2f})")
            
            # Using a unique key for the number_input to prevent auto-reset on rerun
            qty_to_add = st.number_input(f"How many units of {selected_item} do you want?", min_value=0, max_value=min(3, item_details['quantity']), value=0, key=f"qty_input_{selected_item}")

            if qty_to_add > 0:
                if qty_to_add > 3:
                    st.warning("Limit reached. You can only add up to 3 units at a time.")
                    qty_to_add = 3 # Enforce the limit
                
                if qty_to_add > item_details['quantity']:
                    st.error(f"Sorry, only {item_details['quantity']} units of {selected_item} are available.")
                else:
                    if st.button(f"Add {qty_to_add} {selected_item}(s) to cart"):
                        if selected_item in st.session_state.cart:
                            if st.session_state.cart[selected_item]['quantity'] + qty_to_add > 3:
                                st.warning(f"Adding {qty_to_add} more would exceed the 3-unit limit for {selected_item}.")
                            elif st.session_state.cart[selected_item]['quantity'] + qty_to_add > item_details['quantity']:
                                st.error(f"Cannot add {qty_to_add} units. Only {item_details['quantity'] - st.session_state.cart[selected_item]['quantity']} more {selected_item} can be added.")
                            else:
                                st.session_state.cart[selected_item]['quantity'] += qty_to_add
                                st.session_state.total_price += qty_to_add * item_details['price']
                                st.success(f"{qty_to_add} {selected_item}(s) added to cart.")
                                st.rerun() # Rerun to update cart display
                        else:
                            st.session_state.cart[selected_item] = {'quantity': qty_to_add, 'price': item_details['price']}
                            st.session_state.total_price += qty_to_add * item_details['price']
                            st.success(f"{qty_to_add} {selected_item}(s) added to cart.")
                            st.rerun() # Rerun to update cart display

    st.subheader(" Your Cart")
    if not st.session_state.cart:
        st.info("Your cart is empty.")
    else:
        cart_col1, cart_col2, cart_col3, cart_col4 = st.columns([3, 1, 1, 1])
        cart_col1.write("**Item**")
        cart_col2.write("**Qty**")
        cart_col3.write("**Price**")
        cart_col4.write("**Subtotal**")
        st.markdown("---")
        for item, details in st.session_state.cart.items():
            cart_col1.write(item)
            cart_col2.write(details['quantity'])
            cart_col3.write(f"${details['price']:.2f}")
            cart_col4.write(f"${details['quantity'] * details['price']:.2f}")
        st.markdown("---")
        st.write(f"**Total Price: ${st.session_state.total_price:.2f}**")

        if st.button("Proceed to Payment"):
            st.session_state.current_view = 'payment'
            st.rerun()

def payment_view():
    st.title(" Payment Details")
    st.write(f"Your total amount is: **${st.session_state.total_price:.2f}**")

    st.subheader("Select Payment Method:")
    payment_method = st.radio("Choose your payment method:", ('Cash', 'UPI'))

    if st.button("Complete Purchase"):
        # Update groceries quantities
        transaction_details = {
            'items': {},
            'total_amount': st.session_state.total_price,
            'payment_method': payment_method
        }

        for item, details in st.session_state.cart.items():
            if item in st.session_state.groceries:
                st.session_state.groceries[item]['quantity'] -= details['quantity']
                transaction_details['items'][item] = {
                    'quantity_purchased': details['quantity'],
                    'item_price': details['price']
                }

        st.session_state.purchase_history.append(transaction_details)

        # Clear cart after purchase
        st.session_state.cart = {}
        st.session_state.total_price = 0.0

        st.success("Thank you for shopping! Your purchase is complete.")
        st.balloons()
        st.info("Redirecting you to the main store view...")
        st.session_state.current_view = 'customer'
        st.rerun()

    if st.button("Back to Cart"):
        st.session_state.current_view = 'customer'
        st.rerun()

# Function to display store owner view
def owner_view():
    st.title(" Store Owner Dashboard")

    st.subheader("Current Stock Levels:")
    col1, col2, col3 = st.columns([3, 1, 1])
    col1.write("**Item**")
    col2.write("**Qty Left**")
    col3.write("**Price**")
    st.markdown("---")
    for item, details in st.session_state.groceries.items():
        col1.write(item)
        col2.write(details['quantity'])
        col3.write(f"${details['price']:.2f}")

    st.subheader("Purchase History:")
    if not st.session_state.purchase_history:
        st.info("No purchases made yet.")
    else:
        for i, purchase in enumerate(st.session_state.purchase_history):
            st.write(f"**Transaction {i+1}**")
            st.write(f"Payment Method: {purchase['payment_method']}")
            st.write(f"Total Amount: ${purchase['total_amount']:.2f}")
            st.write("Items Purchased:")
            for item, details in purchase['items'].items():
                st.write(f"- {item}: {details['quantity_purchased']} units @ ${details['item_price']:.2f} each")
            st.markdown("---")

    if st.button("Switch to Customer View"):
        st.session_state.current_view = 'customer'
        st.rerun()

# Sidebar for switching views
st.sidebar.title("Navigation")
if st.sidebar.button("Customer View"):
    st.session_state.current_view = 'customer'
    st.rerun()
if st.sidebar.button("Store Owner View"):
    st.session_state.current_view = 'owner'
    st.rerun()

# Display the current view
if st.session_state.current_view == 'customer':
    customer_view()
elif st.session_state.current_view == 'payment':
    payment_view()
elif st.session_state.current_view == 'owner':
    owner_view()