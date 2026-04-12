# Scene definitions
# Each scene is a function that calls connectors to execute a multi-device action
#
# Scenes:
#   leaving     — lock door + close garage + all lights off + AC to eco
#   arriving    — unlock door + entry lights on
#   bedtime     — lock door + check garage + dim bedroom lights + everything else off
#   movie_night — living room lights to 20% + AC to 72F
#   check       — status report: locked? garage closed? lights left on?
