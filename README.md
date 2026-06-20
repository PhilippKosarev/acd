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
$ acd view data.acd
Available items:
  1) aero.ini                    17) drs.ini                    33) suspension_graphics.ini
  2) ai.ini                      18) electronics.ini            34) suspensions.ini
  3) ambient_shadows.ini         19) engine.ini                 35) tcurve_wdt_front.lut
  4) analog_instruments.ini      20) escmode.ini                36) tcurve_wdt_rear.lut
  5) analog_speed_curve.lut      21) fin_AOA_CD.lut             37) throttle.lut
  6) analog_turbo_curve.lut      22) fin_AOA_CL.lut             38) tyres.ini
  7) blurred_objects.ini         23) final.rto                  39) tyres_wdt.lut
  8) brakes.ini                  24) flame_presets.ini          40) wing_animations.ini
  9) cameras.ini                 25) flames.ini                 41) wing_body_AOA_CD.lut
  10) car.ini                    26) lights.ini                 42) wing_body_AOA_CL.lut
  11) colliders.ini              27) lods.ini                   43) wing_front_AOA_CD.lut
  12) damage.ini                 28) mirrors.ini                44) wing_front_AOA_CL.lut
  13) dash_cam.ini               29) power.lut                  45) wing_rear_AOA_CD.lut
  14) digital_instruments.ini    30) proview_nodes.ini          46) wing_rear_AOA_CL.lut
  15) driver3d.ini               31) setup.ini
  16) drivetrain.ini             32) sounds.ini

Select which item to view (1-46, 0 to abort): 2
[GEARS]
UP=6900
DOWN=4000
SLIP_THRESHOLD=0.95
GAS_CUTOFF_TIME=0.300

[PEDALS]
GASGAIN=4.0
BRAKE_HINT=0.87
TRAIL_HINT=0.5

[STEER]
STEER_GAIN=1.61

[LOOKAHEAD]
BASE=17.1
GAS_BRAKE_LOOKAHEAD=10

[HEADER]
VERSION=3

[ULTRA_GRIP]
VALUE=1.2

[PHYSICS_HINTS]
AERO_HINT=1
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
$ acd pack data_dir data.acd
```

To unpack the contents of a .acd file into a directory, you can use `acd unpack`.
```sh
$ acd unpack data.acd data_dir
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
