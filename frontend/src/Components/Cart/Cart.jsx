  import React, { useState, useEffect } from 'react';
  import { useNavigate } from 'react-router-dom';
  import axios from 'axios';
  import './Cart.css';
  import CartCard from './CartCard';

  export default function Cart() {
    const [cartItems, setCartItems] = useState([]);
    const [finalPrice, setFinalPrice] = useState(0);
    const [isAllDeleted, setAllDeleted] = useState(false);

    const navigate = useNavigate();

    

    useEffect(() => {
      const fetchCartAndWatches = async () => {
        try {
          const cartDataMicroservice = await axios.get(import.meta.env.VITE_CART_URL + "/auth/cart/");
          setCartItems(cartDataMicroservice.data);
        } catch (error) {
          console.error('Error fetching cart data:', error);
        }
      };
      fetchCartAndWatches();
    }, [navigate]);

    console.log('Cart Items:', cartItems);

    useEffect(() => {
      if (cartItems.length > 0) {
        const totalPrice = cartItems.reduce((acc, item) => acc + item.final_price, 0);
        setFinalPrice(totalPrice);
      } else {
        setFinalPrice(0);
      }
    }, [cartItems]);

    const removeAllItems = () => {
      if (window.confirm("Are you sure you want to remove all items?")) {
        setAllDeleted(true);
      }
    };

    useEffect(() => {
      if (isAllDeleted) {
        axios.delete(import.meta.env.VITE_CART_URL + "/auth/cart/")
          .then(response => {
            console.log('All items deleted:', response.data);
            setCartItems([]);
            setFinalPrice(0);
            setAllDeleted(false);
          })
          .catch(error => {
            console.error('Error deleting item:', error);
          })
          .finally(() => {
            setAllDeleted(false);
          });
      }
    }, [isAllDeleted]);

    // useEffect(() => {
    //   const total = cartItems.reduce((total, item) => {
    //     const watch = watches.find(watch => watch.id === item.watch_id);
    //     return total + (watch.price * item.quantity);
    //   }, 0);
    //   setFinalPrice(total);
    // }, [cartItems, watches]);


     
     

    return (
      <>
        <div className='container mb-20 flex flex-col lg:flex-row'>
          <div className='cart lg:w-3/5'>
            <div className='header'>
              <h1 className='heading text-xxl'>Cart</h1>
              <button className='remove' onClick={removeAllItems}>
                Remove all
              </button>
            </div>
            {cartItems.length === 0 ? (
              <p>You have nothing in your cart added yet</p>
            ) : (
              <div className='contents'>
                {cartItems.map(item => (
                  <CartCard
                    key={item.id}
                    watchDetails={[item]}
                    onItemDeleted={(deletedItemId) => {
                      setCartItems(prevItems => prevItems.filter(item => item.id !== deletedItemId));
                    }}
                  />
                ))}
              </div>
            )}
            <button className='continue'>
              <a href='/collections'>Continue Shopping</a>
            </button>
          </div>

          <div className='summary mt-10 lg:mt-0 lg:w-2/5'>
            <div className='header'>
              <h1 className='heading text-xxl'>Order Summary</h1>
            </div>
            <div className='summary-contents flex flex-col justify-end mt-8'>
              <div className='details'>
                Shipping Free
              </div>
              <div className='subtotal mb-2'>
                Total: {`$${finalPrice}`}
              </div>
              <button className='order'>Checkout</button>
            </div>
          </div>
        </div>
      </>
    );
  }
