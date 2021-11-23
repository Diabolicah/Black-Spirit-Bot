class CharacterClassCog:
    def __init__(self, bot):
        self.bot = bot


class CharacterClass:
    def __init__(self, character_name="", character_class="", character_level=1, character_ap=0, character_dp=0, character_awakening=0, last_updated=""):
        """Character Constructor"""
        self.character_name = character_name
        self.character_class = character_class
        self.character_level = character_level
        self.character_ap = character_ap
        self.character_dp = character_dp
        self.character_awakening = character_awakening
        self.last_updated = last_updated

    def gear_score(self):
        """Calculates the gear score of a character."""
        return self.character_dp + (self.character_ap if self.character_ap > self.character_awakening else self.character_awakening)

    def fame(self):
        """Calculates Adventurer's Fame"""
        return round(self.character_dp + (self.character_ap + self.character_awakening) / 2)

    def calculated_ap(self):
        fame = self.fame()
        ap = self.character_ap

        if ap >= 309:
            ap = ap + 200
        elif 305 <= ap <= 308:
            ap = ap + 196
        elif 301 <= ap <= 304:
            ap = ap + 188
        elif 297 <= ap <= 300:
            ap = ap + 181
        elif 293 <= ap <= 296:
            ap = ap + 174
        elif 289 <= ap <= 292:
            ap = ap + 167
        elif 285 <= ap <= 288:
            ap = ap + 160
        elif 281 <= ap <= 284:
            ap = ap + 154
        elif 277 <= ap <= 280:
            ap = ap + 148
        elif 273 <= ap <= 276:
            ap = ap + 142
        elif 269 <= ap <= 272:
            ap = ap + 137
        elif 265 <= ap <= 268:
            ap = ap + 122
        elif 261 <= ap <= 264:
            ap = ap + 101
        elif 257 <= ap <= 260:
            ap = ap + 83
        elif 253 <= ap <= 256:
            ap = ap + 69
        elif 249 <= ap <= 252:
            ap = ap + 57
        elif 245 <= ap <= 248:
            ap = ap + 48
        elif 236 <= ap <= 244:
            ap = ap + 40
        elif 201 <= ap <= 235:
            ap = ap + 30
        elif 185 <= ap <= 200:
            ap = ap + 20
        elif 160 <= ap <= 184:
            ap = ap + 10

        if fame > 163:
            ap = ap + 4

        if fame > 211:
            ap = ap + 2
            for tier in range(252, 458, 41):
                print(tier)
                if fame > tier:
                    ap = ap + 2
        if fame > 470:
            ap = ap + 2

        return ap

    def calculated_dp(self):
        fame = self.fame()
        ap = self.character_dp

        if 204 <= ap <= 211:
            ap = ap*1.01
        elif 212 <= ap <= 218:
            ap = ap*1.02
        elif 219 <= ap <= 226:
            ap = ap*1.03
        elif 227 <= ap <= 233:
            ap = ap*1.04
        elif 234 <= ap <= 241:
            ap = ap*1.05
        elif 242 <= ap <= 248:
            ap = ap*1.06
        elif 249 <= ap <= 284:
            ap = ap*1.07
        elif 257 <= ap <= 280:
            ap = ap*1.08
        elif 264 <= ap <= 276:
            ap = ap*1.09
        elif 272 <= ap <= 272:
            ap = ap*1.10
        elif 279 <= ap <= 268:
            ap = ap*1.11
        elif 287 <= ap <= 264:
            ap = ap*1.12
        elif 294 <= ap <= 260:
            ap = ap*1.13
        elif 302 <= ap <= 256:
            ap = ap*1.14
        elif 310 <= ap <= 252:
            ap = ap*1.15
        elif 317 <= ap <= 248:
            ap = ap*1.16
        elif 325 <= ap <= 244:
            ap = ap*1.17
        elif 332 <= ap <= 235:
            ap = ap*1.18
        elif 340 <= ap <= 200:
            ap = ap*1.19
        elif 347 <= ap :
            ap = ap*1.2

        if 123 < fame <= 191:
            ap = ap + 2
        elif 191 < fame <= 232:
            ap = ap + 3
        elif 232 < fame <= 272:
            ap = ap + 4
        elif 272 < fame <= 313:
            ap = ap + 5
        elif 313 < fame <= 354:
            ap = ap +6
        elif 354 < fame <= 395:
            ap = ap + 7
        elif 395 < fame <= 436:
            ap = ap + 8
        elif 436 < fame <= 463:
            ap = ap + 9

        if fame > 463:
            ap = ap + 10
        if fame > 470:
            ap = ap + 5
        if fame > 477:
            ap = ap + 5
        if fame > 484:
            ap = ap + 5
        if fame > 491:
            ap = ap + 5
        if fame > 497:
            ap = ap + 5
        if fame > 504:
            ap = ap + 5
        if fame > 511:
            ap = ap + 5
        if fame > 518:
            ap = ap + 5
        if fame > 525:
            ap = ap + 5
        if fame > 532:
            ap = ap + 5
        if fame > 538:
            ap = ap + 5
        if fame > 545:
            ap = ap + 5
        if fame > 552:
            ap = ap + 5
        if fame > 559:
            ap = ap + 5
        if fame > 566:
            ap = ap + 5
        if fame > 572:
            ap = ap + 5
        if fame > 579:
            ap = ap + 5
        if fame > 586:
            ap = ap + 5
        if fame > 593:
            ap = ap + 5
        if fame > 600:
            ap = ap + 5
        if fame > 606:
            ap = ap + 5
        if fame > 613:
            ap = ap + 5
        if fame > 620:
            ap = ap + 5
        if fame > 627:
            ap = ap + 5
        if fame > 634:
            ap = ap + 5
        if fame > 641:
            ap = ap + 5
        if fame > 647:
            ap = ap + 5

        return round(ap)


def setup(bot):
    bot.add_cog(CharacterClassCog(bot))
