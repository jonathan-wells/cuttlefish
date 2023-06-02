#!/usr/bin/env python3

import sys
import chess
import pygame

WIDTH = HEIGHT = 640
SQUARESIZE = 80
COLORS = [WHITE, BLACK] = chess.COLORS
COLOR_NAMES = ['W', 'B']
RANK_NAMES = chess.RANK_NAMES
FILE_NAMES = chess.FILE_NAMES
PIECE_TYPES = [PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING] = chess.PIECE_TYPES
PIECE_SYMBOLS = chess.PIECE_SYMBOLS


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
    
    def __init__(self, chessgame, image, ptype, color):
        super().__init__()
        self.chessgame = chessgame
        self.screen = self.chessgame.screen
        self.image = image
        self.ptype = ptype
        self.color = color
        self.x = self.y = 0

    def blitme(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = self.x, self.y
        self.screen.blit(self.image, self.rect)

    def current_square(self):
        return FILE_NAMES[int(self.x/80)] + RANK_NAMES[int(self.y/80)]

    def __repr__(self):
        pos = FILE_NAMES[int(self.x/80)] + RANK_NAMES[int(self.y/80)]
        return f'{PIECE_SYMBOLS[self.ptype]}-{COLOR_NAMES[self.color]}-{pos}'


class ChessGame():

    def __init__(self):
        pygame.init()
        pygame.display.set_caption('chess')
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self._load_sprites()
        self._load_board_map()
    
    def _load_board_map(self):
        self.squares = {}
        for i, rank in enumerate(RANK_NAMES[::-1]):
            for j, file in enumerate(FILE_NAMES):
                self.squares[file+rank] = j*SQUARESIZE, i*SQUARESIZE 

    def _load_sprites(self):
        """Cut individual piece sprites from sprite sheet"""
        spritesheet = SpriteSheet()
        self.pieces = {}
        for i, color in enumerate(COLORS):
            for j, ptype in enumerate([KING, 
                                       QUEEN, 
                                       BISHOP, 
                                       KNIGHT,
                                       ROOK,
                                       PAWN]):
                sprite_rect = (j*80, i*80, j*80 + 80, i*80 + 80)
                sprite_img = spritesheet.image_at(sprite_rect)
                if ptype == PAWN:
                    for n in range(8):
                        self.pieces[(ptype, color, n)] = Piece(self, sprite_img, ptype, color)
                elif ptype in (BISHOP, KNIGHT, ROOK):
                    for n in range(2):
                        self.pieces[(ptype, color, n)] = Piece(self, sprite_img, ptype, color)
                else:
                    self.pieces[(ptype, color, 0)] = Piece(self, sprite_img, ptype, color)
                     
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
        for color, rank in [(WHITE, '2'), (BLACK, '7')]:
            for i, file in enumerate(FILE_NAMES):
                piece = self.pieces[(PAWN, color, i)]
                piece.x, piece.y = self.squares[file + rank]
        
        for color, rank in [(WHITE, '1'), (BLACK, '8')]:
            # Rooks
            for n, file in enumerate(['a', 'h']):
                piece = self.pieces[(ROOK, color, n)]
                piece.x, piece.y = self.squares[file + rank]
        
            # Knights
            for n, file in enumerate(['b', 'g']):
                piece = self.pieces[(KNIGHT, color, n)]
                piece.x, piece.y = self.squares[file + rank]
        
            # Bishops
            for n, file in enumerate(['c', 'f']):
                piece = self.pieces[(BISHOP, color, n)]
                piece.x, piece.y = self.squares[file + rank]

        # Queens
            piece = self.pieces[(QUEEN, color, 0)]
            piece.x, piece.y = self.squares['d' + rank]
        
        # Kings
            piece = self.pieces[(KING, color, 0)]
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
    
    def move_piece(self, piece):
        pass

    def run(self):
        self.show_board()
        self.reset_pieces()
        for piece in self.pieces.values():
            print(piece)
        while True:
            self._check_events()
            self._update_screen()
            self.clock.tick(15)

if __name__ == "__main__":
    gui = ChessGame()
    gui.run()
