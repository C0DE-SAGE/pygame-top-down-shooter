from instance import *
import ww
import pygame
import item
import random

class Shop(Instance):
    def __init__(self, pos):
        super().__init__(pos)

        def draw(self, surface):
            text = ww.font20.render(f'웨이브 {ww.wave}', False, (0, 0, 0))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
        item_button = ShopButton(pygame.Rect(10, 320, 80, 30), None, draw)
        ww.group.add(item_button)

        def draw(self, surface):
            text = ww.font20.render(f'골드 {ww.player.gold}', False, (0, 0, 0))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
        item_button = ShopButton(pygame.Rect(100, 320, 80, 30), None, draw)
        ww.group.add(item_button)

        def draw(self, surface):
            text = ww.font20.render(f'스킬포인트 {30}', False, (0, 0, 0))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
        item_button = ShopButton(pygame.Rect(190, 320, 80, 30), None, draw)
        ww.group.add(item_button)

        def draw(self, surface):
            text = ww.font20.render('아이템', False, (0, 0, 0))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
        def callback(s):
            self.phase_set(0)
        item_button = ShopButton(pygame.Rect(100, 10, 80, 30), callback, draw)
        ww.group.add(item_button)

        def draw(self, surface):
            text = ww.font20.render('음식', False, (0, 0, 0))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
        def callback(s):
            self.phase_set(1)
        item_button = ShopButton(pygame.Rect(190, 10, 80, 30), callback, draw)
        ww.group.add(item_button)

        def draw(self, surface):
            text = ww.font20.render('스킬강화', False, (0, 0, 0))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
        def callback(s):
            self.phase_set(2)
        item_button = ShopButton(pygame.Rect(280, 10, 80, 30), callback, draw)
        ww.group.add(item_button)

        def draw(self, surface):
            text = ww.font15.render(f'기본효과', False, (0, 0, 0))
            text_rect = text.get_rect(topleft=pygame.Vector2(self.rect.topleft) + (10, 10))
            surface.blit(text, text_rect)
            text = [
                f'공격력: {round(ww.player.stat.atk, 2)}',
                f'공격속도: {ww.player.stat.atk_firerate}',
                f'이동속도: {ww.player.stat.speed}',
                f'최대체력: {ww.player.stat.mhp}',
                f'투사체 속도: {ww.player.stat.atk_velocity}',
                f'투사체 체공시간: {ww.player.stat.atk_duration}',
                f'치명타 계수: {ww.player.stat.crit}',
                f'치명타 확률: {ww.player.stat.crit_atk}',
                f'골드 획득 계수: {ww.player.stat.gold_earn}',
            ]
            for i, t in enumerate(text):
                t = ww.font12.render(t, False, (0, 0, 0))
                text_rect = t.get_rect(topleft=pygame.Vector2(self.rect.topleft) + (10, 10) + (0, 20 * (i + 1)))
                surface.blit(t, text_rect)
            
            
        item_button = ShopButton(pygame.Rect(460, 10, 170, 300), None, draw)
        ww.group.add(item_button)

        def draw(self, surface):
            text = ww.font20.render(f'다음 웨이브', False, (0, 0, 0))
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)
        def callback(s):
            ww.phase = ww.PHASE.PLAY
            ww.wave += 1
        item_button = ShopButton(pygame.Rect(460, 320, 170, 30), callback, draw)
        ww.group.add(item_button)

        self.phase_button = [
            [], [], []
        ]

        random_numbers = np.random.choice(len(item.items_tier3_name), 4, replace=False)
        items = [item.ItemTier3(number) for number in random_numbers]

        for i in range(4):
            def make_draw(i):
                def draw(self, surface):
                    text = ww.font20.render(f'티어{items[i].tier}', False, (0, 0, 0))
                    text_rect = text.get_rect(center=pygame.Vector2(self.rect.center) - (0, 90))
                    surface.blit(text, text_rect)
                    surface.blit(items[i].image, items[i].rect(center=self.pos - (0, 60)))
                    text = ww.font15.render(f'{items[i].name}', False, (0, 0, 0))
                    text_rect = text.get_rect(center=pygame.Vector2(self.rect.center) - (0, 30))
                    surface.blit(text, text_rect)
                    for j, info in enumerate(items[i].info):
                        text = ww.font15.render(f'{info}', False, (0, 0, 0))
                        text_rect = text.get_rect(center=pygame.Vector2(self.rect.center) - (0, 0 - 15 * j))
                        surface.blit(text, text_rect)
                return draw
            item_button = ShopButton(pygame.Rect(10 + (410 / 4 + 10) * i, 50, 410 / 4, 220), None, make_draw(i))
            self.phase_button[0].append(item_button)
            
            cost = 0
            if items[i].tier == 3:
                cost = 25 + random.randint(-7, 7) + ww.wave
            if items[i].tier == 2:
                cost = 60 + random.randint(-15, 15) + ww.wave * 1.5
            if items[i].tier == 1:
                cost = 100 + random.randint(-22, 22) + ww.wave * 2
            if items[i].tier == 0:
                cost = 120 + ww.wave * 3
            cost = round(cost)

            def make_draw(cost):
                def draw(self, surface):
                    text = ww.font20.render(f'구매 {cost}', False, (0, 0, 0))
                    text_rect = text.get_rect(center=pygame.Vector2(self.rect.center))
                    surface.blit(text, text_rect)
                return draw

            def make_callback(item_button, cost, i):
                def callback(self):
                    if ww.player.gold >= cost:
                        item_button.kill()
                        self.kill()
                        ww.player.gold -= cost
                        ww.player.items_tier3[i] += 1
                        ww.player.apply_item()
                return callback
            
            item_button = ShopButton(pygame.Rect(10 + (410 / 4 + 10) * i, 280, 410 / 4, 30), make_callback(item_button, cost, i), make_draw(cost))
            self.phase_button[0].append(item_button)
            

        self.phase_set(0)

    def phase_set(self, phase):
        self.phase = phase
        for group in self.phase_button:
            for sprite in group:
                sprite.kill()
        for sprite in self.phase_button[phase]:
            ww.group.add(sprite)




class ShopButton(Instance):
    def __init__(self, rect, callback, draw):
        super().__init__(rect.center)
        self.rect = rect
        self.callback = callback
        self.draw_sub = draw

    def update(self):
        if ww.controller.mouse_left_pressed:
            if self.rect.move(ww.view.rect.topleft).collidepoint(ww.controller.mouse_pos):
                if self.callback:
                    self.callback(self)
        if ww.phase != ww.PHASE.SHOP:
            self.kill()
        super().update()

    def draw(self, surface):
        pygame.draw.rect(surface, pygame.Color(255, 255, 255, 192), self.rect)
        self.draw_sub(self, surface)