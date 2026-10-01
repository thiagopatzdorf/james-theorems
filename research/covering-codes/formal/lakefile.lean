import Lake
open Lake DSL

package coveringRecords where
  version := v!"0.1.0"

require CoveringCodes from git
  "https://github.com/florath/covering-codes-lean" @
  "460df105545c2d6b04ba71f29de6b56dbda92825"

lean_lib CoveringRecords
