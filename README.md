Havoc C2 profile generator is a python 3 script that generates profiles to be used with the Havoc C2 Framework.

There are six built in profiles copied from https://github.com/xx0hcd/Malleable-C2-Profiles as a base. I will later on 
move the profiles to a separate directory so you can make JSON configs labelled as such along with the profiles.

The idea of the this generator was to make it extensable and to separate the parts of a profile out to make easy 
randomization if need be. The randomization works by leaving creating a block but leaving it empty as such:
```txt
Operators {
}
```

The script will fill this in with a random username and a random password. Even if the above block is not defined the
script will define the core blocks for you with random data. You can then use the JSON config to only clarify what 
you want to be used either from the profiles or from a completely random generation.

As always I am not responsible for anything done by this script or anyone using this script. Ultimately this is just a
script that generates profiles, which is just text. So don't shoot the messenger.

Have fun!

*Any support is welcome*
