import { Group, Text, Title } from '@mantine/core';

import { SmallCopyButton } from '../SmallCopyButton';

export interface EmojiListItemProps {
  emoji: string;
  emojiName: string;
}

export const EmojiListItem = ({ emoji, emojiName }: EmojiListItemProps) => {
  return (
    <Group gap="lg" px="xs" py="md">
      <Title order={1} component="p" ta="center">
        {emoji}
      </Title>
      <Group justify="space-between" flex={1} miw={0}>
        <Text fw={500} truncate="end" flex={1} tt="capitalize">
          {emojiName}
        </Text>
        <SmallCopyButton value={emoji} />
      </Group>
    </Group>
  );
};
