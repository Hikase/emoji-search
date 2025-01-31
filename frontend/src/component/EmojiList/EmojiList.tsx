import { CopyButton, List, Title, Tooltip } from '@mantine/core';

interface EmojiListProps {
  items: {
    emoji: string;
    emojiName: string;
  }[];
}

export const EmojiList = ({ items }: EmojiListProps) => {
  return (
    <List center spacing="xs" size="md">
      {items.map((item) => (
        <List.Item
          key={item.emoji}
          icon={
            <CopyButton value={item.emoji} timeout={1000}>
              {({ copied, copy }) => (
                <Tooltip
                  label={copied ? 'Copied!' : 'Copy'}
                  withArrow
                  position="left"
                  color={copied ? 'teal' : undefined}
                >
                  <Title order={1} component="p" onClick={copy} style={{ cursor: 'pointer' }}>
                    {item.emoji}
                  </Title>
                </Tooltip>
              )}
            </CopyButton>
          }
        >
          {item.emojiName}
        </List.Item>
      ))}
    </List>
  );
};
