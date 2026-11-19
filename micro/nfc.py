import board
print("testing I2C bus")
i2c = board.I2C()

while not i2c.try_lock():
    pass

i2c.unlock()

print("I2C devices:", [hex(addr) for addr in i2c.scan()])