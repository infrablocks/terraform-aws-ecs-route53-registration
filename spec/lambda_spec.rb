require 'spec_helper'

describe 'IAM policies, profiles and roles' do
  include_context :terraform

  it 'tests' do
    expect(1).to(eq(1))
  end
end