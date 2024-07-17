import pifacecad

wifi = pifacecad.LCDBitmap([14,31,17,14,10,0,4,0])
alarm = pifacecad.LCDBitmap([4,14,14,14,31,0,4,0])

Rain = pifacecad.LCDBitmap([0,14,31,31,31,4,20,12])
Clear = pifacecad.LCDBitmap([4,21,14,31,14,21,4,0])
Wind = pifacecad.LCDBitmap([0,12,16,31,0,31,16,28])
Clouds = pifacecad.LCDBitmap([0,0,14,30,31,31,0,0])#fog
Celsius = pifacecad.LCDBitmap([16,6,9,8,8,9,6,0])

icon = [wifi,alarm,Rain,Clear,Wind,Clouds,Celsius]

def get_icon(status):
    return icon[status]



#cad.lcd.store_custom_bitmap(0, wifi)

#cad.lcd.store_custom_bitmap(1, alarm)

#cad.lcd.store_custom_bitmap(2, rain)
#cad.lcd.store_custom_bitmap(3, clear)
#cad.lcd.store_custom_bitmap(4, wind)
#cad.lcd.store_custom_bitmap(5, clouds)
#cad.lcd.store_custom_bitmap(6, celsius)
