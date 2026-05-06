# acd
A Python library and CLI for reading and writing Assetto Corsa Data (.acd) files.

## Installation
To install the in-development version, run the following:
```sh
pip install git+https://github.com/philippkosarev/acd.git
```
A stable version should be coming soon.

## Documentation
You can find the documentation for the library [here](https://philippkosarev.github.io/acd/).

## Notes about the .acd file format
- .acd files do not have any kind of header or magic number, so it's impossible to check whether a given file is actualy a .acd file, without attempting to read it.
- Moving or renaming a .acd file can make it impossible to decrypt because the encryption key is generated based on either the basename or dirname of the specific file (see the [docs](https://philippkosarev.github.io/acd/acd.get_encryption_key_for_string) for a more in-depth explanation).

## Using the CLI
The acd CLI provides only 3 commands: `view`, `unpack` and `pack`. The names of the commands are pretty self-explanatory, but this is how they work in action:

To view what's inside a .acd file, you can run `acd view`.
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

To pack a directory into a .acd file, you can run `acd pack`.
```sh
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
$ acd pack ./data_dir data.acd
```

To unpack the contents of a .acd file into a directory, you can run `acd unpack`.
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
