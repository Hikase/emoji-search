import { Group, Radio, Text } from '@mantine/core';

import classes from './RadioCard.module.css';

interface RadioCardProps {
  value: string;
  name: string;
  description: string;
}

export const RadioCard = ({ value, name, description }: RadioCardProps) => {
  return (
    <Radio.Card className={classes.root} radius="md" value={value}>
      <Group wrap="nowrap" align="flex-start">
        <Radio.Indicator />
        <div>
          <Text className={classes.label}>{name}</Text>
          <Text className={classes.description}>{description}</Text>
        </div>
      </Group>
    </Radio.Card>
  );
};
