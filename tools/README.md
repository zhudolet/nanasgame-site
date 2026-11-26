# Updating the playable game in /play

`play/` is the browser copy of the game from the `xmas-lights-app` repo (`game/` folder),
with Google Fonts swapped for the local fonts in `play/fonts/` and nothing else changed
(no ads bridge, test mode left as in the source).

To refresh it after the game changes:

    cp -r play/fonts /tmp/xl-fonts
    python3 tools/build_play.py path/to/xmas-lights-app/game play /tmp/xl-fonts

The home page reads the level list from `play/levels/journey-levels-city.js` and talks to
the game through `window.__nl` (`openJIntro`, `openMap`, `LEVELS`, `G`). If the levels file
is renamed, update the `<script src>` near the bottom of `index.html`.

The "Tester tools" button under the phone switches on the game's own test mode
(Prev / Next / Solve / Skip, endless Hot Cocoa). To take it off the public site, delete the
`#tester` button in `index.html`.
