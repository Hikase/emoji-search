import { useState } from 'react';
import { useQuery } from '@siberiacancode/reactuse';

import {
  Anchor,
  Box,
  CloseButton,
  Combobox,
  Highlight,
  Radio,
  ScrollArea,
  Stack,
  TextInput,
  useCombobox,
} from '@mantine/core';
import { useDebouncedValue } from '@mantine/hooks';

import { getAutocompleteOptions } from '@emoji-search/shared/api/autocomplete';

import { RadioCard } from '../RadioCard';

export interface FirstStepProps {
  suggestedEmoji: {
    emoji: string;
    name: string;
    shortcode: string;
  }[];
  value: string;
  onChange: (value: string) => void;
}

interface CustomEmojiComboboxProps {
  value: string;
  onChange: (value: string) => void;
}

const CustomEmojiCombobox = ({ value, onChange }: CustomEmojiComboboxProps) => {
  const [search, setSearch] = useState(value);
  const [debouncedSearch] = useDebouncedValue(search, 500);

  const getAutocompleteQuery = useQuery(
    () => getAutocompleteOptions(debouncedSearch.split(' ').slice(0, 2).at(-1) || ''),
    { keys: [debouncedSearch] }
  );
  const autocompleteResult =
    getAutocompleteQuery.data !== undefined ? getAutocompleteQuery.data.items : [];

  const combobox = useCombobox();

  const options = autocompleteResult.map((item) => (
    <Combobox.Option value={`${item.emoji} ${item.shortcode}`} key={item.emoji}>
      <Highlight highlight={search} size="sm">
        {`${item.emoji} ${item.shortcode}`}
      </Highlight>
    </Combobox.Option>
  ));

  return (
    <Combobox
      onOptionSubmit={(optionValue) => {
        onChange(optionValue);
        setSearch(optionValue);
        combobox.closeDropdown();
      }}
      withinPortal={false}
      store={combobox}
    >
      <Combobox.Target>
        <TextInput
          placeholder="Type emoji shortcode"
          value={search}
          onChange={(event) => {
            combobox.openDropdown();
            combobox.updateSelectedOptionIndex();
            setSearch(event.currentTarget.value);
          }}
          onClick={() => combobox.openDropdown()}
          onFocus={() => combobox.openDropdown()}
          onBlur={() => {
            combobox.closeDropdown();
            setSearch(value);
          }}
          rightSection={
            value !== '' && (
              <CloseButton
                size="sm"
                onMouseDown={(event) => event.preventDefault()}
                onClick={() => {
                  setSearch('');
                  onChange('');
                }}
                aria-label="Clear value"
              />
            )
          }
        />
      </Combobox.Target>

      <Combobox.Dropdown>
        <Combobox.Options>
          <ScrollArea.Autosize mah={200} type="scroll">
            {getAutocompleteQuery.isLoading ? (
              <Combobox.Empty>Loading....</Combobox.Empty>
            ) : options.length === 0 ? (
              <Combobox.Empty>Nothing found</Combobox.Empty>
            ) : (
              options
            )}
          </ScrollArea.Autosize>
        </Combobox.Options>
      </Combobox.Dropdown>
    </Combobox>
  );
};

export const FirstStep = ({ suggestedEmoji, value, onChange }: FirstStepProps) => {
  const [stepType, setStepType] = useState<'suggested' | 'custom'>(
    value === ''
      ? 'suggested'
      : suggestedEmoji.map((item) => `${item.emoji} ${item.shortcode}`).includes(value)
        ? 'suggested'
        : 'custom'
  );

  const toggleFormType = () => {
    setStepType((current) => (current === 'suggested' ? 'custom' : 'suggested'));
  };

  const cards = suggestedEmoji.map((item) => (
    <RadioCard
      key={item.emoji}
      value={`${item.emoji} ${item.shortcode}`}
      name={item.emoji}
      description={item.name}
    />
  ));

  return (
    <Box mt="md" mih={256}>
      {stepType === 'suggested' ? (
        <Radio.Group value={value} onChange={onChange}>
          <Stack gap="xs">{cards}</Stack>
        </Radio.Group>
      ) : (
        <CustomEmojiCombobox value={value} onChange={onChange} />
      )}
      <Anchor component="button" type="button" onClick={toggleFormType} size="sm" mt="md">
        {stepType === 'suggested'
          ? 'Do you think there is a more relevant emoji? Please suggest!'
          : 'Return to suggested emoji.'}
      </Anchor>
    </Box>
  );
};
