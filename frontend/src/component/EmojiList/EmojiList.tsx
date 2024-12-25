import { Divider } from '@mantine/core';

import { EmojiListItem, EmojiListItemProps } from './EmojiListItem';

interface EmojiListProps {
  itemsData: EmojiListItemProps[];
}

export const EmojiList = ({ itemsData }: EmojiListProps) => {
  return itemsData.map((item, index) => (
    <>
      <EmojiListItem key={item.emoji} emoji={item.emoji} emojiName={item.emojiName} />
      {index !== itemsData.length - 1 && <Divider />}
    </>
  ));
};
