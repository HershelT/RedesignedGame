#   OLD CODE TO make the block player was on have the player sprite built in but nothing else changed
#Fixed it by making blocks and entities different
          # #Draw the player over the block we are about to step on
            # chunkBlock = copy.deepcopy(Chunk.getBlock(PLAYER.getChunk(), (PLAYER.getX(), PLAYER.getY())).getSprite())
            # chunkBlock = addToScreenWithoutColor(chunkBlock, PLAYER.getSprite(), BACKGROUND_COLOR, 0, 0, True)
            # #Make the player step on the block
            # Chunk.setBlock(PLAYER.getChunk(), (PLAYER.getX(), PLAYER.getY()), Block(PLAYER.getBlockBehind().getName(), chunkBlock))
