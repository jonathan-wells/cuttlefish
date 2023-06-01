#!/usr/bin/env python3

import sys
import chess
import pygame

WIDTH = HEIGHT = 640
SQUARESIZE = 80



class SpriteSheet():
    
    def __init__(self):
        self.sheet = pygame.image.load('../img/Chess_Pieces_Sprite.png').convert_alpha()
    
    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface((SQUARESIZE, SQUARESIZE), pygame.SRCALPHA)
        image.blit(self.sheet, (0, 0), rect)
        if colorkey != None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image


class Piece(pygame.sprite.Sprite):
    
    def __init__(self, chessgame, image, name, color):
        super().__init__()
        self.chessgame = chessgame
        self.screen = self.chessgame.screen
        self.image = image
        self.name = name
        self.color = color

        self.x = self.y = 0

    def blitme(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        self.screen.blit(self.image, self.rect)


class ChessGame():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('chess')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self._load_sprites()
        self._load_board_map()
    
    def _load_board_map(self):
        self.files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.ranks = ['1', '2', '3', '4', '5', '6', '7', '8']
        self.squares = {}
        for i, rank in enumerate(self.ranks[::-1]):
            for j, file in enumerate(self.files):
                self.squares[file+rank] = j*SQUARESIZE, i*SQUARESIZE 

    def _load_sprites(self):
        """Cut individual piece sprites from sprite sheet"""
        spritesheet = SpriteSheet()
        colors = ['W', 'B']
        pieces = ['K', 'Q', 'B', 'N', 'R', 'p']
        self.pieces = {}
        
        for i, color in enumerate(colors):
            for j, piece_name in enumerate(pieces):
                sprite_rect = (j*80, i*80, j*80 + 80, i*80 + 80)
                sprite_img = spritesheet.image_at(sprite_rect)
                if piece_name == 'p':
                    for k in range(8):
                        self.pieces[(piece_name + str(k+1), color)] = Piece(self, sprite_img, piece_name, color)
                elif piece_name in ('B', 'N', 'R'):
                    for k in range(2):
                        self.pieces[(piece_name + str(k+1), color)] = Piece(self, sprite_img, piece_name, color)
                else:
                    self.pieces[(piece_name, color)] = Piece(self, sprite_img, piece_name, color)
                     

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def _update_screen(self):
        for piece in self.pieces.values():
            piece.blitme()
        pygame.display.flip()

    def reset_pieces(self):
        """Reset all piece sprites to starting positions"""
        # Pawns
        for i, file in enumerate(self.files):
            piece_name = 'p' + str(i+1)
            for color, rank in [('W', '2'), ('B', '7')]:
                piece = self.pieces[(piece_name, color)]
                piece.x, piece.y = self.squares[file + rank]
        
        # Rooks
        for piece_name, file in [('R1', 'a'), ('R2', 'h')]:
            for color, rank in [('W', '1'), ('B', '8')]:
                piece = self.pieces[(piece_name, color)]
                piece.x, piece.y = self.squares[file + rank]
        
        # Knights
        for piece_name, file in [('N1', 'b'), ('N2', 'g')]:
            for color, rank in [('W', '1'), ('B', '8')]:
                piece = self.pieces[(piece_name, color)]
                piece.x, piece.y = self.squares[file + rank]
        
        # Bishops
        for piece_name, file in [('B1', 'c'), ('B2', 'f')]:
            for color, rank in [('W', '1'), ('B', '8')]:
                piece = self.pieces[(piece_name, color)]
                piece.x, piece.y = self.squares[file + rank]

        # Queens
        for color, rank in [('W', '1'), ('B', '8')]:
            piece = self.pieces[('Q', color)]
            piece.x, piece.y = self.squares['d' + rank]
        
        # Kings
        for color, rank in [('W', '1'), ('B', '8')]:
            piece = self.pieces[('K', color)]
            piece.x, piece.y = self.squares['e' + rank]
            
    def show_board(self):
        for rank in range(8):
            for file in range(8):
                if (rank + file) % 2 == 0: 
                    square_color = 236, 208, 166  # White 
                else:
                    square_color = 165, 117, 80  # Black
                square = (rank*SQUARESIZE, 
                          file*SQUARESIZE, 
                          SQUARESIZE,
                          SQUARESIZE)
                pygame.draw.rect(self.screen, square_color, square)

    def run(self):
        self.show_board()
        self.reset_pieces()
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(15)

if __name__ == "__main__":
    gui = ChessGame()
    gui.run()
