import pika

params = pika.URLParameters('amqps://woqqzdfw:yB1qus3DYDHTFimwiycxmB0HGZEPDGwZ@puffin.rmq2.cloudamqp.com/woqqzdfw')

connection = pika.BlockingConnection(params)
channel = connection.channel()

def publish(product_id, brand, name, price):
    message = f"Product added to cart: {product_id,brand,name,price}"
    channel.basic_publish(exchange='', routing_key='admin', body=message)
    print(f" [x] Sent {message}")
