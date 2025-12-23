# acd
A python library and cli for reading and writing Assetto Corsa Data (.acd) files.

## Installing
```sh
pip install git+https://github.com/PhilippKosarev/acd.git
```

## Using the CLI
Viewing what's inside the `data.acd` file:
```sh
$ acd view ./data.acd
Available files:
  1) aero.ini                  2) ai.ini                  3) ambient_shadows.ini
  4) analog_instruments.ini    5) analog_speed_curve.lut  6) blurred_objects.ini
  7) brakes.ini                8) cameras.ini             9) car.ini
  10) colliders.ini            11) damage.ini             12) dash_cam.ini
  13) digital_instruments.ini  14) driver3d.ini           15) drivetrain.ini
  16) electronics.ini          17) engine.ini             18) escmode.ini
  19) final.rto                20) fin_AOA_CD.lut         21) fin_AOA_CL.lut
  22) fuel_cons.ini            23) lights.ini             24) lods.ini
  25) mirrors.ini              26) power.lut              27) proview_nodes.ini
  28) setup.ini                29) sounds.ini             30) suspensions.ini
  31) suspension_graphics.ini  32) tcurve_wdt_front.lut   33) tcurve_wdt_rear.lut
  34) throttle.lut             35) tyres.ini              36) tyres_wdt.lut
  37) wing_animations.ini      38) wing_body_AOA_CD.lut   39) wing_body_AOA_CL.lut
  40) wing_front_AOA_CD.lut    41) wing_front_AOA_CL.lut  42) wing_rear_AOA_CD.lut
  43) wing_rear_AOA_CL.lut

Input which file to view (1-43, 0 to abort): 25
mirrors.ini:
[MIRROR_0]
NAME=mirrorL

[MIRROR_1]
NAME=mirrorR

[MIRROR_2]
NAME=mirrorC
```

Unpacking the `data.acd` file to a directory:
```sh
$ acd unpack ./data.acd data_dir
$ ls data_dir
aero.ini                 electronics.ini          suspensions.ini
ai.ini                   engine.ini               tcurve_wdt_front.lut
ambient_shadows.ini      escmode.ini              tcurve_wdt_rear.lut
analog_instruments.ini   final.rto                throttle.lut
analog_speed_curve.lut   fin_AOA_CD.lut           tyres.ini
blurred_objects.ini      fin_AOA_CL.lut           tyres_wdt.lut
brakes.ini               fuel_cons.ini            wing_animations.ini
cameras.ini              lights.ini               wing_body_AOA_CD.lut
car.ini                  lods.ini                 wing_body_AOA_CL.lut
colliders.ini            mirrors.ini              wing_front_AOA_CD.lut
damage.ini               power.lut                wing_front_AOA_CL.lut
dash_cam.ini             proview_nodes.ini        wing_rear_AOA_CD.lut
digital_instruments.ini  setup.ini                wing_rear_AOA_CL.lut
driver3d.ini             sounds.ini
drivetrain.ini           suspension_graphics.ini
```

Packing a directory into a `data.acd` file:
```sh
$ acd pack ./data_dir data-2.acd
```

## Using the library
The acd library exposes only 2 functions: `read_file` and `write_file`.

Here is a simple example where we read a file and print the first value:
```python
import acd
input_file = './data.acd'
data = acd.read_file(input_file)
keys = list(data.keys())
first_key = keys[0]
print(data.get(first_key))
```

Here is a simple example on how to write a file:
```python
import acd
output_file = './data.acd'
data = {'example-filename.txt': 'Hello from the example-filename.txt!'}
acd.write_file(output_file, data)
```

## Note about the .acd file format
The encryption key is generated based on the basename or the dirname of the .acd file, so renaming the file or moving it to a directory with a different name will make it impossible to decrypt the file.