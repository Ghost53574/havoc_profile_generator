Havoc C2 profile generator is a python3 script that generates profiles to be used with the Havoc C2 Framework.

There are six built in profiles copied from https://github.com/xx0hcd/Malleable-C2-Profiles as a base. You can 
now parse Cobalt Strike profiles using this tool (I only need to add a couple of additional checks, but it works).

The idea of this generator was to make it extensible and to separate the parts of a profile out to make easy 
randomization if need be. The randomization works by leaving creating a block but leaving it empty as such.

The script will fill this in with a random username and a random password. Even if the above block is not defined the
script will define the core blocks for you with random data. You can then use the JSON config to only clarify what 
you want to be used either from the profiles or from a completely random generation.

This is the sample config
```json
{
}
```
![havoc_profile_generator](https://github.com/Ghost53574/havoc_profile_generator/assets/5248937/9a85caa8-9be4-4282-a045-92d2625ba0ed)

And using the generated profile with Havoc C2

![havoc_c2](https://github.com/Ghost53574/havoc_profile_generator/assets/5248937/f8d07d09-30d1-4977-85fb-80716fc38fab)

As always I am not responsible for anything done by this script or anyone using this script. Ultimately this is just a
script that generates profiles, which is just text. So don't shoot the messenger.

I regularely review the Havoc C2 source code for changes on how I can better utilize this script for automation.

Thank you to C5Spider for the cool logo design that I turned into ICE styled text. 

Have fun!
