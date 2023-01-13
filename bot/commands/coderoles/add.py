from discord import Color

from bot.base import Command
from bot.config import Config, Embed


class cmd(Command):
    """A discord command instance."""

    ### Allowed languages and max allowed code roles per user ###
    code_roles_color = Color.from_rgb(137, 204, 240)
    max_code = 5
    whitelist = [
        "Ada",
        "Assembly",
        "APL",
        "Basic",
        "Brainfuck",
        "C",
        "C++",
        "C#",
        "Dart",
        "F#",
        "Fortran",
        "Go",
        "Groovy",
        "Haskell",
        "HTML/CSS",
        "IDL",
        "Java",
        "Javascript",
        "Julia",
        "Kotlin",
        "Lisp",
        "Lua",
        "Lustre",
        "MATLAB",
        "NXC",
        "Objective-C",
        "OCaml",
        "Pascal",
        "PHP",
        "Python",
        "Perl",
        "QML",
        "R",
        "Ruby",
        "Rust",
        "Scala",
        "Shell",
        "Solidity",
        "Swift",
        "SQL",
        "TeX",
        "Typescript",
        "VBA",
        "XSLT",
        "YaBasic",
        "Zig",
    ]

    name = "add"
    usage = "add <language>"
    description = f"Assigns user a role based on selected languages, max of {max_code} code roles per user."

    ### Gets Role Object with from a given name ###
    def getRole(self, message, role_name):
        for role in message.guild.roles:
            if role.name == role_name:
                return role

    async def execute(self, arguments, message) -> None:
        user_roles_names = []
        server_roles_names = []
        name = message.author.name

        for role in message.author.roles:
            user_roles_names.append(role.name)
        for role in message.guild.roles:
            server_roles_names.append(role.name)

        # Checks if role is whitelisted
        if arguments[0].lower() not in map(lambda lang: lang.lower(), self.whitelist):
            embed = Embed(
                title="Code",
                description="**Invalid language**\n\n*To see valid languages, use:*\n`v!code whitelist`",
            )
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return
        # Checks if user already has the role
        if arguments[0].lower() in map(lambda role: role.lower(), user_roles_names):
            embed = Embed(
                title="Code", description=f"**`{name}` already has that code role**"
            )
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return
        # Checks if user has maximum code roles
        max = 0
        for role in user_roles_names:
            if role in self.whitelist:
                max += 1
        if max >= self.max_code:
            embed = Embed(
                title="Code",
                description=f"**`{name}` has reached the max code roles.**\n\n*To see your current code roles, use:*\n`v!code roles` \n\n*To remove a code role, use:*\n`v!code remove [Your language]`",
            )
            embed.set_color("red")
            await message.channel.send(embed=embed)
            return

        role_name = self.whitelist[
            list(map(lambda lang: lang.lower(), self.whitelist)).index(
                arguments[0].lower()
            )
        ]
        # Checks if role exists, if not, creates role
        if role_name not in server_roles_names:
            await message.guild.create_role(
                name=role_name, colour=self.code_roles_color
            )
        # Adds user to role
        role = self.getRole(message, role_name)
        await message.author.add_roles(role)
        embed = Embed(
            title="Code",
            description=f"**`{name}` has been added to the `{role.name}` code role**",
        )
        await message.channel.send(embed=embed)
